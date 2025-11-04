from django.shortcuts import render, redirect, get_object_or_404
from LoginRegister.models import Ensayo
from .models import Ensayo, Pregunta, Tema, Tag
from .forms import EnsayoForm, PreguntaForm, TemaForm, TagForm
from AutoridadDocente.models import RespuestaEnsayo, RespuestaPregunta
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.db import IntegrityError


def index(request):
    return render(request, 'base_docente.html')

def home_docente(request):
    return render(request, 'home_docente.html')



def ensayos_view(request):
    ensayos = Ensayo.objects.all()
    return render(request, 'ensayos_docente.html', {'ensayos': ensayos})

def cuentadoc_view(request):
    return render(request, 'cuenta_docente.html')

def listar_ensayos(request):
    ensayos = Ensayo.objects.all()
    return render(request, 'ensayos/listar.html', {'ensayos': ensayos})

def crear_tema(request):
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')  # redirige a un nombre de URL que sí existe
    else:
        form = TemaForm()
    return render(request, 'crear_tema.html', {'form': form})

def crear_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('listar_preguntas')
            except IntegrityError:
                # Defensa extra ante carreras o casos raros
                form.add_error('name', 'Ya existe una etiqueta con un slug derivado de ese nombre. Intenta con otro nombre.')
    else:
        form = TagForm()
    return render(request, 'crear_tag.html', {'form': form})


def crear_ensayo(request):
    if request.method == 'POST':
        form = EnsayoForm(request.POST)
        if form.is_valid():
            ensayo = form.save(commit=False)
            ensayo.save()
            
            # Manejar nuevo tema
            nuevo_tema_nombre = form.cleaned_data.get('nuevo_tema')
            if nuevo_tema_nombre:
                nuevo_tema, created = Tema.objects.get_or_create(nombre=nuevo_tema_nombre)
                ensayo.temas.add(nuevo_tema)
            
            form.save_m2m()  # Para guardar relaciones many-to-many
            return redirect('listar_ensayos')
    else:
        form = EnsayoForm()
    return render(request, 'ensayos/formulario.html', {'form': form})

def editar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    if request.method == 'POST':
        form = EnsayoForm(request.POST, instance=ensayo)
        if form.is_valid():
            ensayo = form.save(commit=False)
            ensayo.save()
            
            nuevo_tema_nombre = form.cleaned_data.get('nuevo_tema')
            if nuevo_tema_nombre:
                nuevo_tema, created = Tema.objects.get_or_create(nombre=nuevo_tema_nombre)
                ensayo.temas.add(nuevo_tema)
            
            form.save_m2m()
            return redirect('listar_ensayos')
    else:
        form = EnsayoForm(instance=ensayo)
    return render(request, 'ensayos/formulario.html', {'form': form})

def eliminar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    ensayo.delete()
    return redirect('listar_ensayos')

def listar_preguntas(request):
    solo_libres = request.GET.get('libres') == '1'
    preguntas = Pregunta.objects.all().prefetch_related('temas')
    if solo_libres and hasattr(Pregunta, 'is_free'):
        preguntas = preguntas.filter(is_free=True)

    context = {
        'preguntas': preguntas,
        'solo_libres': solo_libres,
    }
    return render(request, 'preguntas/listar.html', context)

def crear_pregunta(request):
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')
    else:
        form = PreguntaForm()
    return render(request, 'preguntas/formulario.html', {'form': form})

def editar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    if request.method == 'POST':
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')
    else:
        form = PreguntaForm(instance=pregunta)
    return render(request, 'preguntas/formulario.html', {'form': form})

def eliminar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    pregunta.delete()
    return redirect('listar_preguntas')

@login_required
def resultados_ensayos_docente(request):
    if request.user.role != 'AutoridadDocente':
        return redirect('login')

    resultados = RespuestaEnsayo.objects.select_related('estudiante', 'ensayo').order_by('-fecha_respuesta')
    return render(request, 'resultados/resultados_docente.html', {'resultados': resultados})


@login_required
def graficos_docente(request):
    # Solo docentes
    if getattr(request.user, "role", None) != 'AutoridadDocente':
        return redirect('login')

    # === Saneo de parámetros ===
    raw_tag_ids = request.GET.getlist('tags', [])
    parsed_ids, invalid_vals = [], []
    for v in raw_tag_ids:
        try:
            parsed_ids.append(int(v))
        except (TypeError, ValueError):
            invalid_vals.append(v)

    # Eliminar duplicados preservando orden
    seen = set()
    dedup_ids = []
    for i in parsed_ids:
        if i not in seen:
            dedup_ids.append(i)
            seen.add(i)

    # Límite máximo de etiquetas aplicadas
    MAX_TAGS = 5
    truncated = len(dedup_ids) > MAX_TAGS
    limited_ids = dedup_ids[:MAX_TAGS]

    # Verificar cuáles existen realmente en BD
    existing_ids = list(
        Tag.objects.filter(id__in=limited_ids).values_list('id', flat=True)
    )
    missing_ids = [i for i in limited_ids if i not in existing_ids]

    # Preparar avisos de filtro
    filter_warnings = []
    if invalid_vals:
        filter_warnings.append(f"Se ignoraron {len(invalid_vals)} ID(s) de etiqueta inválidos.")
    if missing_ids:
        filter_warnings.append(f"Se ignoraron {len(missing_ids)} etiqueta(s) inexistentes.")
    if truncated:
        filter_warnings.append(f"Se aplicó un máximo de {MAX_TAGS} etiquetas; el resto fue ignorado.")

    # Cargar catálogo completo para checkboxes
    tags = Tag.objects.all().order_by('name')

    data_labels = []
    data_correctas = []
    data_incorrectas = []
    total_global = 0
    agg_rows = []

    if existing_ids:
        qs = (
            RespuestaPregunta.objects
            .filter(pregunta__tags__in=existing_ids)
            .values('pregunta__tags__id', 'pregunta__tags__name')
            .annotate(
                total=Count('id'),
                correctas=Count('id', filter=Q(alternativa_elegida=F('pregunta__respuesta_correcta')))
            )
            .order_by('pregunta__tags__name')
        )

        for row in qs:
            nombre = row['pregunta__tags__name']
            total = row['total'] or 0
            correctas = row['correctas'] or 0
            incorrectas = max(total - correctas, 0)

            data_labels.append(nombre)
            data_correctas.append(correctas)
            data_incorrectas.append(incorrectas)
            total_global += total

            agg_rows.append({
                'name': nombre,
                'correctas': correctas,
                'incorrectas': incorrectas,
                'total': total,
            })

    context = {
        'tags': tags,
        # Solo marcar como seleccionadas las etiquetas existentes y saneadas
        'selected_tag_ids': existing_ids,
        'data_labels': data_labels,
        'data_correctas': data_correctas,
        'data_incorrectas': data_incorrectas,
        'total_global': total_global,
        'agg': agg_rows,
        'filter_warnings': filter_warnings,
        'max_tags': MAX_TAGS,
    }
    return render(request, 'graficos.html', context)
