import csv

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.next = None
        self.prev = None
        self.sub_list = None


class Doublelinkedlist:
    def __init__(self):
        self.head = None
        self.tail = None

    def search_by_attr(self, attr, value):
        current = self.head
        while current:
            if getattr(current, attr) == value:
                return current
            current = current.next
        return None

    def add_child(self, parent, child):
        if parent.sub_list is None:
            sublist = Doublelinkedlist()
            sublist.head = child
            sublist.tail = child
            parent.sub_list = sublist
        else:
            current = parent.sub_list.tail
            current.next = child
            child.prev = current
            parent.sub_list.tail = child
        return parent.sub_list
    
    def print_multilist(self, level=0):
        if self.head is None:
            print("Empty list")
            return

        current = self.head
        while current:
            print("  " * level + str(current))
            if current.sub_list:
                current.sub_list.print_multilist(level + 1)
            current = current.next

    def append(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node


class Level1(Node):
    def __init__(self, id, name):
        super().__init__(id, name)

    def __str__(self):
        return f"Level1: {self.name}"


class Level2(Node):
    def __init__(self, id, name):
        super().__init__(id, name)

    def __str__(self):
        return f"Level2: {self.name}"


class Level3(Node):
    def __init__(self, id, name):
        super().__init__(id, name)

    def __str__(self):
        return f"Level3: {self.name}"


class Level4(Node):
    def __init__(self, id, name):
        super().__init__(id, name)

    def __str__(self):
        return f"Level4: {self.name}"


def cargar_datos_csv(file_path):
    datos = Doublelinkedlist()
    current_l1 = None
    current_l2 = None
    current_l3 = None

    with open(file_path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            id_l1 = row["id_l1"]
            name_l1 = row["name_l1"]
            if id_l1 == "":
                continue

            id_l1 = int(id_l1)
            if current_l1 is None or id_l1 != current_l1.id:
                current_l1 = Level1(id_l1, name_l1)
                datos.append(current_l1)
                current_l2 = None
                current_l3 = None

            id_l2 = row["id_l2"]
            if id_l2 != "":
                id_l2 = int(id_l2)
                name_l2 = row["name_l2"]
                if current_l2 is None or id_l2 != current_l2.id:
                    current_l2 = Level2(id_l2, name_l2)
                    datos.add_child(current_l1, current_l2)
                    current_l3 = None

                id_l3 = row["id_l3"]
                if id_l3 != "":
                    id_l3 = int(id_l3)
                    name_l3 = row["name_l3"]
                    if current_l3 is None or id_l3 != current_l3.id:
                        current_l3 = Level3(id_l3, name_l3)
                        datos.add_child(current_l2, current_l3)

                    id_l4 = row["id_l4"]
                    if id_l4 != "":
                        id_l4 = int(id_l4)
                        name_l4 = row["name_l4"]
                        l4 = Level4(id_l4, name_l4)
                        datos.add_child(current_l3, l4)

    return datos


def buscar_por_id(datos, node_id):
    current_l1 = datos.head
    
    while current_l1:
        if current_l1.sub_list:
            current_l2 = current_l1.sub_list.head
            while current_l2:
                if current_l2.sub_list:
                    current_l3 = current_l2.sub_list.head
                    while current_l3:
                        if current_l3.sub_list:
                            nodo = current_l3.sub_list.search_by_attr("id", node_id)
                            if nodo:
                                return nodo, current_l1, current_l2, current_l3
                        current_l3 = current_l3.next
                current_l2 = current_l2.next
        current_l1 = current_l1.next
    
    return None, None, None, None


if __name__ == "__main__":
    datos = cargar_datos_csv("empresas.csv")
    print("=== Estructura cargada ===\n")
    datos.print_multilist()
    
    print("\n=== Búsqueda ===\n")
    node_id = 1001
    nodo, l1, l2, l3 = buscar_por_id(datos, node_id)
    
    if nodo:
        print(f"Nodo encontrado: {nodo.name} (ID: {nodo.id})")
        print(f"  Nivel 1: {l1.name}")
        print(f"  Nivel 2: {l2.name}")
        print(f"  Nivel 3: {l3.name}")
    else:
        print(f"Nodo con ID {node_id} no encontrado")


        ##

def cargar_datos_csv(file_path):
    """Carga el CSV DIVIPOLA y construye una multilist: Pais -> Departamento -> Municipio."""
    datos = Doublelinkedlist()

    # Creamos un nodo Pais único para Colombia
    pais = Pais("CO", "COLOMBIA")
    datos.append(pais)

    with open(file_path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Campos según el CSV proporcionado
            codigo_depto = row.get("Código Departamento", "").strip()
            nombre_depto = row.get("Nombre Departamento", "").strip()
            codigo_mun = row.get("Código Municipio", "").strip()
            nombre_mun = row.get("Nombre Municipio", "").strip()

            if codigo_depto == "" or codigo_mun == "":
                continue

            # Buscar departamento existente
            dept = None
            if pais.sub_list:
                dept = pais.sub_list.search_by_attr("id", codigo_depto)

            if dept is None:
                dept = Departamento(codigo_depto, nombre_depto)
                datos.add_child(pais, dept)

            # Agregar municipio bajo el departamento
            # Evitamos duplicados simples buscando por id en la sublista
            exists = False
            if dept.sub_list:
                exists = dept.sub_list.search_by_attr("id", codigo_mun) is not None

            if not exists:
                mun = Municipio(codigo_mun, nombre_mun)
                datos.add_child(dept, mun)

    return datos


def buscar_municipio_por_codigo(datos, codigo_mun):
    """Busca un municipio por su código y devuelve (municipio, departamento, pais)"""
    pais = datos.head
    while pais:
        if pais.sub_list:
            dept = pais.sub_list.head
            while dept:
                if dept.sub_list:
                    mun = dept.sub_list.search_by_attr("id", codigo_mun)
                    if mun:
                        return mun, dept, pais
                dept = dept.next
        pais = pais.next
    return None, None, None


if __name__ == "__main__":
    datos = cargar_datos_csv("DIVIPOLA-_C_digos_municipios_20250505.csv")
    print("=== Estructura cargada ===\n")
    datos.print_multilist()

    print("\n=== Búsqueda ejemplo ===\n")
    codigo = "05001"  # ejemplo: Medellín
    mun, dept, pais = buscar_municipio_por_codigo(datos, codigo)
    if mun:
        print(f"Municipio encontrado: {mun.name} (ID: {mun.id})")
        print(f"  Departamento: {dept.name}")
        print(f"  Pais: {pais.name}")
    else:
        print(f"Municipio con código {codigo} no encontrado")