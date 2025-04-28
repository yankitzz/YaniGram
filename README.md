# YaniGram: Instagram Likes & Following Scraper

YaniGram es una herramienta sencilla en Python para **extraer los usuarios que han dado like a tus publicaciones de Instagram** y también para **extraer la lista de tus seguidos**. Los resultados se guardan en archivos de texto para que puedas analizarlos o utilizarlos como prefieras.

---

## 🚀 Características
- Extrae todos los usuarios que han dado like a tus últimas publicaciones.
- Guarda los resultados en un archivo de texto (`usuarios_likes.txt`).
- Extrae la lista de cuentas que sigues (seguidos) y la guarda en un archivo de texto (`seguidos.txt`).
- Interfaz por consola, fácil de usar.
- Proceso lento y controlado para evitar bloqueos de Instagram.

---

## ⚙️ Requisitos
- Python 3.8 o superior
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/) (opcional si usas `webdriver-manager`)

Instala las dependencias con:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Uso
1. **Activa el entorno virtual** (si usas uno):
   ```bash
   venv\Scripts\activate  # En Windows
   # o
   source venv/bin/activate  # En Mac/Linux
   ```

2. **Ejecuta el script:**
   ```bash
   python instagram.py
   ```

3. **Sigue las instrucciones en pantalla:**
   - Ingresa tu usuario y contraseña de Instagram.
   - Elige si quieres extraer likes de la última, penúltima, antepenúltima publicación o de las tres.
   - El script guardará los usuarios en `usuarios_likes.txt` y los seguidos en `seguidos.txt`.

---

## 📂 Archivos generados
- `usuarios_likes.txt`: Usuarios que dieron like a tus publicaciones.
- `seguidos.txt`: Lista de tus seguidos.

---

## 📝 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## ⚠️ Aviso
- **No compartas tus credenciales de Instagram.**
- El uso de este script es solo para fines personales y educativos.
- El uso excesivo puede violar los términos de servicio de Instagram. Úsalo bajo tu propio riesgo.

---

## ✨ Autor
Creado por [Tu Nombre o Alias]. ¡Contribuciones y sugerencias son bienvenidas!
