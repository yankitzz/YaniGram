# --- IMPORTS ---
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

# --- FUNCIONES PRINCIPALES ---
def entrar_ultima_publicacion(driver):
    """Hace clic en la última publicación del perfil."""
    try:
        wait = WebDriverWait(driver, 10)
        posts = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_aagw")))
        if posts:
            posts[0].click()
            print("Haz hecho clic en tu última publicación.")
            return True
        else:
            print("No se encontraron publicaciones.")
            return False
    except Exception as e:
        print(f"Error al intentar hacer clic en la última publicación: {e}")
        return False

def entrar_penultima_publicacion(driver):
    """Hace clic en la penúltima publicación del perfil."""
    try:
        wait = WebDriverWait(driver, 10)
        posts = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_aagw")))
        if len(posts) > 1:
            posts[1].click()
            print("Haz hecho clic en tu penúltima publicación.")
            return True
        else:
            print("No hay suficientes publicaciones para seleccionar la penúltima.")
            return False
    except Exception as e:
        print(f"Error al intentar hacer clic en la penúltima publicación: {e}")
        return False

def entrar_antepenultima_publicacion(driver):
    """Hace clic en la antepenúltima publicación del perfil."""
    try:
        wait = WebDriverWait(driver, 10)
        posts = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_aagw")))
        if len(posts) > 2:
            posts[2].click()
            print("Haz hecho clic en tu antepenúltima publicación.")
            return True
        else:
            print("No hay suficientes publicaciones para seleccionar la antepenúltima.")
            return False
    except Exception as e:
        print(f"Error al intentar hacer clic en la antepenúltima publicación: {e}")
        return False

def ir_a_perfil(driver, usuario):
    url = f"https://www.instagram.com/{usuario}/"
    print(f"Navegando al perfil: {url}")
    driver.get(url)
    print("Esperando a que cargue el perfil...")
    time.sleep(5)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_aagw"))
        )
        print("Perfil cargado correctamente.")
    except Exception:
        print("Advertencia: No se detectó el grid de publicaciones, puede que el perfil no haya cargado completamente.")
    time.sleep(2)

def ver_likes_publicacion(driver):
    """Navega al enlace de likes, espera la carga y extrae todos los usuarios con scroll."""
    time.sleep(2)
    publicacion_url = driver.current_url
    publicacion_url = publicacion_url.split('?img_index=1')[0]
    enlace_likes = publicacion_url.rstrip('/') + '/liked_by/'
    print(f"Navegando al enlace de likes: {enlace_likes}")
    driver.get(enlace_likes)
    print("Esperando a que cargue la página de likes...")
    time.sleep(5)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span._ap3a._aaco._aacw._aacx._aad7._aade'))
        )
        print("Usuarios de likes visibles. Esperando 2 segundos antes de hacer scroll...")
    except Exception:
        print("Advertencia: No se detectaron usuarios de likes, puede que la página no haya cargado completamente.")
    time.sleep(2)
    return extraer_todos_los_usuarios_likes_pagina(driver)

def extraer_todos_los_usuarios_likes_pagina(driver, max_scrolls=100):
    """Hace scroll en la página completa hasta cargar todos los usuarios y los extrae usando BeautifulSoup."""
    print("Haciendo scroll para cargar todos los usuarios...")
    last_count = 0
    scrolls = 0
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        spans = soup.find_all('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade')
        usuarios = [span.get_text(strip=True) for span in spans if span.get_text(strip=True)]
        print(f"Usuarios detectados tras scroll {scrolls}: {len(usuarios)}")
        if len(usuarios) == last_count or scrolls >= max_scrolls:
            print("Scroll finalizado.")
            break
        last_count = len(usuarios)
        scrolls += 1
        print("Realizando scroll lento...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    print(f"[BS4] Usuarios extraídos tras scroll ({len(usuarios)}):")
    for usuario in usuarios:
        print(usuario)
    return usuarios

def extraer_todos_los_seguidos(driver, max_scrolls=100):
    """
    Hace clic en el botón de 'Seguidos', abre la ventana modal y hace scroll hasta el final para cargar todos los seguidos.
    Imprime en consola el progreso y avisa cuando llega al final del scroll.
    """
    print("Abriendo la ventana de seguidos...")
    try:
        seguidos = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a/span')
        seguidos.click()
        time.sleep(2)
        scroll_box = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
        last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        scrolls = 0
        while True:
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_box)
            time.sleep(1.5)
            new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
            print(f"Scroll {scrolls}: altura {new_height}")
            if new_height == last_height:
                print("Fin del scroll: todos los seguidos han sido cargados.")
                break
            last_height = new_height
            scrolls += 1
            if scrolls >= max_scrolls:
                print("Límite de scroll alcanzado.")
                break
        # Extraer los nombres de usuario usando BeautifulSoup para mayor robustez
        html = scroll_box.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        spans = soup.find_all('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade')
        usuarios_seguidos = [span.get_text(strip=True) for span in spans if span.get_text(strip=True)]
        print(f"Total de seguidos extraídos: {len(usuarios_seguidos)} (usando BeautifulSoup)")
        for usuario in usuarios_seguidos:
            print(usuario)
        return usuarios_seguidos
    except Exception as e:
        print(f"Error al extraer seguidos: {e}")
        return []

def login_instagram(driver, usuario, contraseña):
    print("Iniciando sesión en Instagram...")
    try:
        driver.get('https://www.instagram.com/')
        time.sleep(2)
        aceptar_cookies = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]')
        aceptar_cookies.click()
        time.sleep(3)
        user_input = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
        user_input.click()
        user_input.send_keys(usuario)
        time.sleep(3)
        pass_input = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
        pass_input.click()
        pass_input.send_keys(contraseña)
        aceptar = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button/div')
        aceptar.click()
        time.sleep(5)
        if "login" in driver.current_url:
            print("❌ Credenciales incorrectas o captcha requerido.")
            return False
        print("✅ Inicio de sesión exitoso.")
        print("Esperando unos segundos en la pantalla de inicio...")
        time.sleep(5)  # Espera adicional en la pantalla de inicio antes de continuar
        return True
    except Exception as e:
        print(f"❌ Error durante el inicio de sesión: {e}")
        return False

def menu_accion():
    print("""
¿Qué acción quieres realizar?
1. Extraer likes de la última publicación
2. Extraer likes de la penúltima publicación
3. Extraer likes de la antepenúltima publicación
4. Extraer likes de las 3 últimas publicaciones
5. Extraer seguidos
""")
    return input("Selecciona una opción (1-5): ")

def guardar_usuarios_txt(usuarios, nombre_archivo='usuarios_likes.txt'):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta absoluta de la carpeta YaniGram
    carpeta = os.path.join(base_dir, 'datos_extraidos')
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        for usuario in usuarios:
            f.write(usuario + '\n')
    print(f"Usuarios guardados en {ruta_archivo} ({len(usuarios)} usuarios).")

# --- FLUJO PRINCIPAL ---
if __name__ == '__main__':
    tu_usuario = input("Escribe tu usuario: ")
    tu_contraseña = getpass.getpass("Escribe tu contraseña: ")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    if not login_instagram(driver, tu_usuario, tu_contraseña):
        exit(1)

    time.sleep(3)
    driver.get(f"https://www.instagram.com/{tu_usuario}/")
    while True:
        opcion = menu_accion()
        usuarios_total = set()
        try:
            if opcion == '1':
                print("Extrayendo likes de la última publicación...")
                ir_a_perfil(driver, tu_usuario)
                entrar_ultima_publicacion(driver)
                usuarios_total.update(ver_likes_publicacion(driver))
            elif opcion == '2':
                print("Extrayendo likes de la penúltima publicación...")
                ir_a_perfil(driver, tu_usuario)
                entrar_penultima_publicacion(driver)
                usuarios_total.update(ver_likes_publicacion(driver))
            elif opcion == '3':
                print("Extrayendo likes de la antepenúltima publicación...")
                ir_a_perfil(driver, tu_usuario)
                entrar_antepenultima_publicacion(driver)
                usuarios_total.update(ver_likes_publicacion(driver))
            elif opcion == '4':
                print("Extrayendo likes de las 3 últimas publicaciones...")
                for funcion, nombre in [
                    (entrar_ultima_publicacion, 'última'),
                    (entrar_penultima_publicacion, 'penúltima'),
                    (entrar_antepenultima_publicacion, 'antepenúltima')
                ]:
                    print(f"Procesando {nombre} publicación...")
                    ir_a_perfil(driver, tu_usuario)
                    funcion(driver)
                    usuarios_total.update(ver_likes_publicacion(driver))
                usuarios_total = set(usuarios_total)
            elif opcion == '5':
                print("Extrayendo seguidos...")
                ir_a_perfil(driver, tu_usuario)
                seguidos = extraer_todos_los_seguidos(driver)
                guardar_usuarios_txt(seguidos, nombre_archivo='seguidos.txt')
                print("✅ Seguidos extraídos y guardados en seguidos.txt.")
                continue
            else:
                print("Opción no válida.")
                continue
            print(f"Total de usuarios extraídos: {len(usuarios_total)}")
            guardar_usuarios_txt(usuarios_total)
            print("✅ Proceso finalizado.")
        except Exception as e:
            print(f"❌ Error durante la extracción: {e}")
            print("Puedes intentar de nuevo.")
            continue
        otra = input("¿Deseas hacer otra extracción? (s/n): ").strip().lower()
        if otra != 's':
            print("¡Hasta luego!")
            break
