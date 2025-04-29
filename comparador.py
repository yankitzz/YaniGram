import os

def leer_usuarios_desde_txt(path):
    """
    Lee un archivo de texto y devuelve un set de usuarios (uno por línea, sin espacios extra).
    """
    with open(path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def comparar_listas(archivo_base, archivo_comparar, descripcion_base, descripcion_comparar):
    """
    Compara dos archivos de usuarios y muestra:
    - Usuarios en base que NO están en comparar (por ejemplo, seguidos que no han dado like)
    - Usuarios en comparar que NO están en base (por ejemplo, likes de gente que no sigues)
    """
    usuarios_base = leer_usuarios_desde_txt(archivo_base)
    usuarios_comparar = leer_usuarios_desde_txt(archivo_comparar)

    print(f"\nUsuarios en '{descripcion_base}' que NO están en '{descripcion_comparar}':")
    faltantes = usuarios_base - usuarios_comparar
    for usuario in sorted(faltantes):
        print(usuario)
    print(f"Total: {len(faltantes)}\n")

    print(f"Usuarios en '{descripcion_comparar}' que NO están en '{descripcion_base}':")
    extras = usuarios_comparar - usuarios_base
    for usuario in sorted(extras):
        print(usuario)
    print(f"Total: {len(extras)}\n")

def seguidos_que_no_dieron_like(seguidos, *likes_archivos):
    """
    Devuelve los usuarios de seguidos que NO han dado like a ninguna de las publicaciones indicadas.
    """
    seguidos_set = leer_usuarios_desde_txt(seguidos)
    likes_total = set()
    for archivo in likes_archivos:
        likes_total.update(leer_usuarios_desde_txt(archivo))
    return seguidos_set - likes_total

def seguidos_que_no_dieron_like_a(seguidos, likes_archivo):
    """
    Devuelve los usuarios de seguidos que NO han dado like a la publicación del archivo indicado.
    """
    seguidos_set = leer_usuarios_desde_txt(seguidos)
    likes_set = leer_usuarios_desde_txt(likes_archivo)
    return seguidos_set - likes_set

def quienes_me_dieron_like_y_no_sigo(seguidos, likes_archivo):
    """
    Devuelve usuarios que me dieron like pero yo NO los sigo.
    """
    seguidos_set = leer_usuarios_desde_txt(seguidos)
    likes_set = leer_usuarios_desde_txt(likes_archivo)
    return likes_set - seguidos_set

def fans_que_no_sigo(seguidos, likes1, likes2, likes3):
    """
    Devuelve usuarios que han dado like a las 3 últimas publicaciones y que NO sigues (tus 'fans').
    """
    seguidos_set = leer_usuarios_desde_txt(seguidos)
    likes_1 = leer_usuarios_desde_txt(likes1)
    likes_2 = leer_usuarios_desde_txt(likes2)
    likes_3 = leer_usuarios_desde_txt(likes3)
    fans = likes_1 & likes_2 & likes_3
    return fans - seguidos_set

def guardar_resultado_txt(usuarios, descripcion):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base_dir, 'datos_extraidos')
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = f"resultado_{descripcion}.txt"
    ruta = os.path.join(carpeta, nombre_archivo)
    with open(ruta, 'w', encoding='utf-8') as f:
        for usuario in sorted(usuarios):
            f.write(usuario + '\n')
    print(f"Resultado guardado en {ruta} ({len(usuarios)} usuarios).\n")

def archivos_requeridos_faltantes(archivos_dict):
    faltan = []
    for path, sugerencia in archivos_dict.items():
        if not os.path.exists(path):
            faltan.append(sugerencia)
    return faltan

def menu_comparador():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datos_dir = os.path.join(base_dir, 'datos_extraidos')
    print("\n=== COMPARADOR DE USUARIOS ===")
    archivos = [f for f in os.listdir(datos_dir) if f.endswith('.txt')]
    for idx, archivo in enumerate(archivos, 1):
        print(f"{idx}. {archivo}")
    print("\nOpciones avanzadas:")
    print("a. Seguidos que NO han dado like a NINGUNA de las 3 publicaciones")
    print("b. Seguidos que NO han dado like a la última publicación")
    print("c. Usuarios que SÍ me dieron like y yo NO los sigo (en la última publicación)")
    print("d. Comparación personalizada (elige 2 archivos)")
    print("e. Ver mis fans (usuarios que han dado like a las 3 últimas publicaciones y yo NO los sigo)")
    opcion = input("\nSelecciona una opción (número o letra): ").strip().lower()
    if opcion == 'a':
        arch_seguidos = os.path.join(datos_dir, 'seguidos.txt')
        arch_likes1 = os.path.join(datos_dir, 'likes_ultima_publicacion.txt')
        arch_likes2 = os.path.join(datos_dir, 'likes_penultima_publicacion.txt')
        arch_likes3 = os.path.join(datos_dir, 'likes_antepenultima_publicacion.txt')
        archivos_dict = {
            arch_seguidos: "Extraer seguidos",
            arch_likes1: "Extraer likes de la última publicación",
            arch_likes2: "Extraer likes de la penúltima publicación",
            arch_likes3: "Extraer likes de la antepenúltima publicación"
        }
        faltan = archivos_requeridos_faltantes(archivos_dict)
        if faltan:
            print("\nFaltan los siguientes archivos necesarios:")
            for sugerencia in faltan:
                print(f"- {sugerencia}")
            print("Por favor, realiza primero la(s) extracción(es) correspondiente(s) en el menú principal.")
            time.sleep(3)
            return
        resultado = seguidos_que_no_dieron_like(arch_seguidos, arch_likes1, arch_likes2, arch_likes3)
        print("\nSeguidos que NO han dado like a NINGUNA de las 3 publicaciones:")
        for usuario in sorted(resultado):
            print(usuario)
        print(f"Total: {len(resultado)}\n")
        if input("¿Guardar resultado en archivo? (s/n): ").strip().lower() == 's':
            guardar_resultado_txt(resultado, 'seguidos_no_like_ninguna')
    elif opcion == 'b':
        arch_seguidos = os.path.join(datos_dir, 'seguidos.txt')
        arch_likes = os.path.join(datos_dir, 'likes_ultima_publicacion.txt')
        archivos_dict = {
            arch_seguidos: "Extraer seguidos",
            arch_likes: "Extraer likes de la última publicación"
        }
        faltan = archivos_requeridos_faltantes(archivos_dict)
        if faltan:
            print("\nFaltan los siguientes archivos necesarios:")
            for sugerencia in faltan:
                print(f"- {sugerencia}")
            print("Por favor, realiza primero la(s) extracción(es) correspondiente(s) en el menú principal.")
            time.sleep(3)
            return
        resultado = seguidos_que_no_dieron_like_a(arch_seguidos, arch_likes)
        print("\nSeguidos que NO han dado like a la ÚLTIMA publicación:")
        for usuario in sorted(resultado):
            print(usuario)
        print(f"Total: {len(resultado)}\n")
        if input("¿Guardar resultado en archivo? (s/n): ").strip().lower() == 's':
            guardar_resultado_txt(resultado, 'seguidos_no_like_ultima')
    elif opcion == 'c':
        arch_seguidos = os.path.join(datos_dir, 'seguidos.txt')
        arch_likes = os.path.join(datos_dir, 'likes_ultima_publicacion.txt')
        archivos_dict = {
            arch_seguidos: "Extraer seguidos",
            arch_likes: "Extraer likes de la última publicación"
        }
        faltan = archivos_requeridos_faltantes(archivos_dict)
        if faltan:
            print("\nFaltan los siguientes archivos necesarios:")
            for sugerencia in faltan:
                print(f"- {sugerencia}")
            print("Por favor, realiza primero la(s) extracción(es) correspondiente(s) en el menú principal.")
            time.sleep(3)
            return
        resultado = quienes_me_dieron_like_y_no_sigo(arch_seguidos, arch_likes)
        print("\nUsuarios que SÍ me dieron like y yo NO los sigo (en la última publicación):")
        for usuario in sorted(resultado):
            print(usuario)
        print(f"Total: {len(resultado)}\n")
        if input("¿Guardar resultado en archivo? (s/n): ").strip().lower() == 's':
            guardar_resultado_txt(resultado, 'me_dieron_like_no_sigo_ultima')
    elif opcion == 'd':
        print("\nSelecciona el archivo BASE (por ejemplo, tus seguidos):")
        idx_base = int(input("Número archivo base: ")) - 1
        print("Selecciona el archivo para comparar (por ejemplo, likes de una publicación):")
        idx_comp = int(input("Número archivo comparar: ")) - 1
        archivo_base = os.path.join(datos_dir, archivos[idx_base])
        archivo_comp = os.path.join(datos_dir, archivos[idx_comp])
        descripcion_base = archivos[idx_base]
        descripcion_comp = archivos[idx_comp]
        comparar_listas(archivo_base, archivo_comp, descripcion_base, descripcion_comp)
        # Opción de guardar no implementada aquí porque puede ser ambigua
    elif opcion == 'e':
        arch_seguidos = os.path.join(datos_dir, 'seguidos.txt')
        arch_likes1 = os.path.join(datos_dir, 'likes_ultima_publicacion.txt')
        arch_likes2 = os.path.join(datos_dir, 'likes_penultima_publicacion.txt')
        arch_likes3 = os.path.join(datos_dir, 'likes_antepenultima_publicacion.txt')
        archivos_dict = {
            arch_seguidos: "Extraer seguidos",
            arch_likes1: "Extraer likes de la última publicación",
            arch_likes2: "Extraer likes de la penúltima publicación",
            arch_likes3: "Extraer likes de la antepenúltima publicación"
        }
        faltan = archivos_requeridos_faltantes(archivos_dict)
        if faltan:
            print("\nFaltan los siguientes archivos necesarios:")
            for sugerencia in faltan:
                print(f"- {sugerencia}")
            print("Por favor, realiza primero la(s) extracción(es) correspondiente(s) en el menú principal.")
            return
        resultado = fans_que_no_sigo(arch_seguidos, arch_likes1, arch_likes2, arch_likes3)
        print("\nTus FANS (usuarios que han dado like a tus 3 últimas publicaciones y tú NO los sigues):")
        for usuario in sorted(resultado):
            print(usuario)
        print(f"Total: {len(resultado)}\n")
        if input("¿Guardar resultado en archivo? (s/n): ").strip().lower() == 's':
            guardar_resultado_txt(resultado, 'fans_no_sigo')
    else:
        print("Opción no válida.")

if __name__ == '__main__':
    menu_comparador()
