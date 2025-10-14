import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from LoginRegister.models import User
from AutoridadDocente.models import (
    Ensayo, Pregunta, Tema, Tag,
    RespuestaEnsayo, RespuestaPregunta
)

class TestCrearEnsayoEndpoint(TestCase):
    """
    Endpoint: /docente/ensayos/crear/
    Dos casos:
      - válido: 302 tras crear
      - inválido: 200 con errores (falta título)
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.client = None
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # Usuario docente para autenticación
        cls.doc = User.objects.create_user(
            username="docente_test",
            password="x123456",
            role="AutoridadDocente",
        )
        # Elegimos un nivel válido desde las choices
        cls.nivel_valido = User.NIVELES[0][0] if hasattr(User, "NIVELES") else "Media"

    def setUp(self):
        # Autenticación de docente para cada prueba
        self.client.login(username="docente_test", password="x123456")

    def test_crear_ensayo_valido_redirige(self):
        """
        Equivalencia: datos válidos mínimos -> redirect (302)
        Input: titulo, nivel válido, colegio
        Output: 302
        """
        url = reverse("crear_ensayo")
        payload = {
            "titulo": "Ensayo desde test",
            "nivel": self.nivel_valido,
            "colegio": "SIP",
            # temas/preguntas son opcionales en el form actual
        }
        resp = self.client.post(url, data=payload, follow=False)
        self.assertEqual(resp.status_code, 302)

        # sanity check: el objeto se creó
        self.assertTrue(Ensayo.objects.filter(titulo="Ensayo desde test").exists())

    def test_crear_ensayo_invalido_muestra_errores(self):
        """
        Frontera: falta campo obligatorio 'titulo' -> 200 con errores
        Input: sin titulo
        Output: 200 y form con error en 'titulo'
        """
        url = reverse("crear_ensayo")
        payload = {
            # "titulo" ausente
            "nivel": self.nivel_valido,
            "colegio": "SIP",
        }
        resp = self.client.post(url, data=payload)
        self.assertEqual(resp.status_code, 200)
        # Verificamos errores de form en contexto
        self.assertIn("form", resp.context)
        self.assertIn("titulo", resp.context["form"].errors)


class TestGraficosEndpoint(TestCase):
    """
    Endpoint: /docente/graficos/
    Dos casos:
      - sin autenticación/rol -> redirect (302)
      - docente + datos por etiqueta -> 200 y contexto correcto
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.client = None
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # Docente y Estudiante para poblar datos
        cls.doc = User.objects.create_user(
            username="docente_graf",
            password="x123456",
            role="AutoridadDocente",
        )
        cls.est = User.objects.create_user(
            username="est_graf",
            password="x123456",
            role="Estudiante",
        )

        # Datos mínimos para una etiqueta con 1 respuesta correcta
        cls.tema = Tema.objects.create(nombre="Geometría")
        cls.tag = Tag.objects.create(name="Geo", slug="geo")

        cls.p = Pregunta.objects.create(
            enunciado="¿Pregunta Geo?",
            opciones={'A':'a','B':'b','C':'c','D':'d'},
            respuesta_correcta='A',
            is_free=True
        )
        cls.p.temas.add(cls.tema)
        cls.p.tags.add(cls.tag)

        cls.ensayo = Ensayo.objects.create(
            titulo="Ensayo Geo",
            nivel=User.NIVELES[0][0] if hasattr(User, "NIVELES") else "Media",
            colegio="SIP"
        )
        cls.ensayo.preguntas.add(cls.p)

        re = RespuestaEnsayo.objects.create(
            estudiante=cls.est,
            ensayo=cls.ensayo,
            fecha_respuesta=timezone.now(),
            puntaje=100
        )
        RespuestaPregunta.objects.create(
            respuesta_ensayo=re,
            pregunta=cls.p,
            alternativa_elegida='A'  # correcta
        )

    def test_graficos_sin_login_redirige(self):
        """
        Control de acceso: sin autenticación -> 302 a login
        """
        url = reverse("graficos_docente")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (301, 302))

    def test_graficos_docente_ok_con_datos(self):
        """
        Equivalencia: docente + etiqueta -> 200, template correcto y contexto consistente
        """
        self.client.login(username="docente_graf", password="x123456")
        url = reverse("graficos_docente")
        resp = self.client.get(url, {"tags": [self.tag.id]})
        self.assertEqual(resp.status_code, 200)

        # template (ajusta si usas subcarpeta distinta)
        self.assertTemplateUsed(resp, "graficos.html")

        ctx = resp.context
        self.assertEqual(ctx["data_labels"], [self.tag.name])
        self.assertEqual(ctx["data_correctas"], [1])
        self.assertEqual(ctx["data_incorrectas"], [0])
        self.assertEqual(ctx["total_global"], 1)
