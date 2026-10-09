import pygame
from settings import *

class SistemaRespuestas:
    def __init__(self, franja_img):
        self.activo = False
        self.cofre_actual = None
        self.respuesta_actual = ""
        self.jugador = None

        self.ancho = ANCHO - 100
        self.alto = 160

        if franja_img:
            self.fondo = pygame.transform.scale(franja_img, (self.ancho, self.alto))
        else:
            self.fondo = pygame.Surface((self.ancho, self.alto))
            self.fondo.fill((60, 60, 90))

        self.font = pygame.font.Font(None, 36)
        self.font_peq = pygame.font.Font(None, 24)
        print("✓ Sistema de respuestas inicializado")

    def activar(self, cofre, jugador=None):
        """Activa el sistema para un cofre específico"""
        if self.activo:
            return  # Ya hay un cofre activo

        self.activo = True
        self.cofre_actual = cofre  # Guarda la referencia al cofre específico
        self.respuesta_actual = ""
        self.jugador = jugador

        print(f"📝 Activado para cofre en ({cofre.rect.x}, {cofre.rect.y})")
        print(f"📝 Operación: {cofre.operacion} = {cofre.respuesta_correcta}")
        print(f"📝 Estado: abierto={cofre.abierto}, resuelto={cofre.resuelto}")

    def desactivar(self):
        """Desactiva el sistema completamente"""
        self.activo = False
        self.cofre_actual = None
        self.respuesta_actual = ""
        self.jugador = None

    def manejar_evento(self, evento, jugador, franja):
        """Maneja eventos de teclado para el sistema de respuestas"""
        if not self.activo or not self.cofre_actual:
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # Verificar respuesta SOLO para el cofre actual
                if self.respuesta_actual:
                    try:
                        valor = int(self.respuesta_actual)

                        # Verificar que el cofre actual existe y no está resuelto
                        if (self.cofre_actual and
                            not self.cofre_actual.resuelto and
                            valor == self.cofre_actual.respuesta_correcta):

                            # Marcar ESTE cofre específico como resuelto
                            self.cofre_actual.resuelto = True
                            self.cofre_actual.operacion_resuelta = True

                            # Añadir operación al jugador
                            if jugador and hasattr(jugador, 'operaciones'):
                                operacion_str = f"{self.cofre_actual.operacion} = {self.cofre_actual.respuesta_correcta}"
                                if operacion_str not in jugador.operaciones:
                                    jugador.operaciones.append(operacion_str)
                                    print(f"✅ Operación añadida: {operacion_str}")
                                    print(f"📊 Operaciones totales: {len(jugador.operaciones)}/3")

                            franja.mostrar(f"¡Correcto! {self.cofre_actual.operacion} = {self.cofre_actual.respuesta_correcta}", duracion=2.0)
                        else:
                            franja.mostrar(f"Incorrecto. Intenta de nuevo.", duracion=1.5)

                    except ValueError:
                        franja.mostrar("Número inválido", duracion=1.5)

                self.desactivar()
                return True

            elif evento.key == pygame.K_ESCAPE:
                self.desactivar()
                franja.mostrar("Cancelado", duracion=1.0)
                return True

            elif evento.key == pygame.K_BACKSPACE:
                self.respuesta_actual = self.respuesta_actual[:-1]
                return True

            elif evento.unicode.isdigit():
                if len(self.respuesta_actual) < 4:
                    self.respuesta_actual += evento.unicode
                return True

        return False

    def actualizar(self):
        """Actualiza el sistema (se llama cada frame)"""
        # Si el cofre actual ya está resuelto, desactivar
        if self.activo and self.cofre_actual and self.cofre_actual.resuelto:
            self.desactivar()

    def dibujar(self, pantalla):
        """Dibuja la interfaz del sistema de respuestas"""
        if not self.activo or not self.cofre_actual:
            return

        # Verificar que el cofre no esté ya resuelto
        if self.cofre_actual.resuelto:
            self.desactivar()
            return

        # Fondo semi-transparente
        fondo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 160))
        pantalla.blit(fondo, (0, 0))

        # Panel principal
        x = (ANCHO - self.ancho) // 2
        y = (ALTO - self.alto) // 2
        pantalla.blit(self.fondo, (x, y))

        # Borde del panel
        pygame.draw.rect(pantalla, TEXTO_TITULO, (x-2, y-2, self.ancho+4, self.alto+4), 3)

        # Título
        titulo = self.font.render("Resuelve la operación:", True, TEXTO_TITULO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO//2, y + 30)))

        # Operación específica del cofre actual
        if hasattr(self.cofre_actual, 'obtener_texto_operacion'):
            operacion_texto = self.cofre_actual.obtener_texto_operacion()
        else:
            operacion_texto = f"{self.cofre_actual.operacion} = ?"

        txt_op = self.font.render(operacion_texto, True, TEXTO_OPERACION)
        pantalla.blit(txt_op, txt_op.get_rect(center=(ANCHO//2, y + 70)))

        # Línea debajo de la operación
        pygame.draw.line(pantalla, TEXTO_SECUNDARIO,
                        (ANCHO//2 - 100, y + 85),
                        (ANCHO//2 + 100, y + 85), 1)

        # Respuesta del usuario
        respuesta_texto = self.respuesta_actual if self.respuesta_actual else "_"
        txt_resp = self.font.render(respuesta_texto, True, TEXTO_RESPUESTA)
        pantalla.blit(txt_resp, txt_resp.get_rect(center=(ANCHO//2, y + 110)))

        # Instrucciones
        instrucciones = self.font_peq.render("ENTER: Enviar | ESC: Cancelar | BACKSPACE: Borrar", True, TEXTO_SECUNDARIO)
        pantalla.blit(instrucciones, instrucciones.get_rect(center=(ANCHO//2, y + 140)))
