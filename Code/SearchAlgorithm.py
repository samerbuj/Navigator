# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1490885'
__group__ = 'DL.15'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy

# Human speed represented by HUMAN_SPEED
HUMAN_SPEED = 5

def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []

    """for conn in map.connections[path.last]:
        new_path = copy.deepcopy(path)
        new_path.add_route(conn)
        path_list.append(new_path)"""

    for conn in map.connections[path.last].keys():  # Más rápido que con deepcopy
        aux = path.route[:]
        aux.append(conn)
        new_path = Path(aux)
        new_path.g = path.g
        new_path.h = path.h
        new_path.f = path.f
        path_list.append(new_path)

    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    for p in reversed(path_list):  # Si no fuera reversed, joderíamos los índices
        stations = []
        for x in p.route:
            if x not in stations:
                stations.append(x)
            else:
                path_list.remove(p)

    return path_list


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return expand_paths + list_of_path

    pass


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    llista = [Path(origin_id)]

    while (llista[0].route[-1] != destination_id) and (llista is not None):
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        llista = insert_depth_first_search(E, llista)

    if llista[0].route[-1] == destination_id:
        return llista[0]
    else:
        print("No existeix Solucio")

    pass


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return list_of_path + expand_paths

    pass


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista = [Path(origin_id)]

    while (llista[0].route[-1] != destination_id) and (llista is not None):
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        llista = insert_breadth_first_search(E, llista)

    if llista[0].route[-1] == destination_id:
        print_list_of_path(llista)
        return llista[0]
    else:
        print("No existeix Solucio")

    pass


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    if type_preference == 0:
        for ruta in expand_paths:
            ruta.update_g(1)

    elif type_preference == 1:
        for ruta in expand_paths:
            ruta.update_g(map.connections[ruta.penultimate][ruta.last])

    elif type_preference == 2:
        for ruta in expand_paths:
            if map.stations[ruta.penultimate]['name'] != map.stations[ruta.last]['name']:
                ruta.update_g(map.connections[ruta.penultimate][ruta.last] * map.velocity[map.stations[ruta.last]['line']]) #tiempo * velocidad de la línea de llegada

    elif type_preference == 3:
        for ruta in expand_paths:
            if map.stations[ruta.penultimate]['line'] != map.stations[ruta.last]['line']:
                ruta.update_g(1)

    return expand_paths

    pass


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    #  Consultar si mi método es suficientemente eficiente
    #  usaré sort() en lugar de sorted() porque el segundo retorna la lista ordenada, pero no modifica el orden original

    lista = list_of_path + expand_paths
    #  print_list_of_path_with_cost(sorted(lista, key=lambda path: path.g))
    return sorted(lista, key=lambda path: path.g)

    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista = [Path(origin_id)]

    while (llista[0].route[-1] != destination_id) and (llista is not None):
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        E = calculate_cost(E, map, type_preference)
        llista = insert_cost(E, llista)

    if llista[0].route[-1] == destination_id:
        return llista[0]
    else:
        print("No existeix Solucio")

    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    if type_preference == 0:
        for ruta in expand_paths:
            if ruta.last != destination_id:
                ruta.update_h(1)
            else:
                ruta.update_h(0)

    elif type_preference == 1:
        max_vel = 0

        for i in range(1, len(map.velocity)):
            new_vel = map.velocity[i]
            if new_vel > max_vel:
                max_vel = new_vel

        coord_dest = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]

        for ruta in expand_paths:
            coord_orig = [map.stations[ruta.last]['x'], map.stations[ruta.last]['y']]
            # coordenadas de la última estación de la ruta
            distance = euclidean_dist(coord_orig, coord_dest)
            ruta.update_h(distance/max_vel)

    elif type_preference == 2:
        coord_dest = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]

        for ruta in expand_paths:
            coord_orig = [map.stations[ruta.last]['x'], map.stations[ruta.last]['y']]
            # coordenadas de la última estación de la ruta
            distance = euclidean_dist(coord_orig, coord_dest)
            ruta.update_h(distance)

    elif type_preference == 3:
        line_dest = map.stations[destination_id]['line']

        for ruta in expand_paths:
            if map.stations[ruta.last]['line'] != line_dest:
                ruta.update_h(1)
            else:
                ruta.update_h(0)

    return expand_paths

    pass


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for ruta in expand_paths:
        ruta.update_f()

    return expand_paths

    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): All visited stations cost updated
    """
    for ruta_exp in reversed(expand_paths):
        if ruta_exp.last in visited_stations_cost.keys():
            if ruta_exp.g >= visited_stations_cost[ruta_exp.last]:
                expand_paths.remove(ruta_exp)
            else:
                visited_stations_cost[ruta_exp.last] = ruta_exp.g

        for ruta in reversed(list_of_path):
            if ruta_exp.head == ruta.head and ruta_exp.last == ruta.last:
                # ruta_exp.head == ruta.head and #TÉCNICAMENTE NO HACE FALTA COMPROBAR, YA QUE EL ORIGEN DEBERÍA SER EL MISMO
                if ruta_exp.g < ruta.g:
                    if ruta in list_of_path:
                        list_of_path.remove(ruta)
                    visited_stations_cost[ruta.last] = ruta_exp.g
                else:
                    if ruta_exp in expand_paths:
                        expand_paths.remove(ruta_exp)

    return expand_paths, list_of_path, visited_stations_cost

    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    lista = list_of_path + update_f(expand_paths)
    # print_list_of_path_with_cost(sorted(lista, key=lambda path: path.f))

    return sorted(lista, key=lambda path: path.f)

    pass


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """

    possible_origins = []

    min_dist = INF

    for station in range(1, len(map.stations) + 1):
        station_coord = [map.stations[station]["x"], map.stations[station]["y"]]
        station_dist = euclidean_dist(coord, station_coord)

        if station_dist < min_dist:
            min_dist = station_dist
            possible_origins.clear()
            possible_origins.append(station)

        elif station_dist == min_dist:
            possible_origins.append(station)

    return possible_origins

    pass


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    lista_origen = coord2station(origin_coor, map)
    lista_destino = coord2station(dest_coor, map)

    llista = [Path(lista_origen[0])]
    destination_id = lista_destino[0]
    TCP = {}  # se supone que esto es un diccionario de costes de las estaciones

    while (llista[0].last != destination_id) and (llista is not None):
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        E = calculate_cost(E, map, type_preference)
        E = calculate_heuristics(E, map, destination_id, type_preference)
        remove_redundant_paths(E, llista, TCP)
        llista = insert_cost_f(E, llista)

    if llista[0].route[-1] == destination_id:
        return llista[0]
    else:
        print("No existeix Solucio")

    pass


###############################
# ESTO YA ES PARTE DEL OPCIONAL
###############################


def coord2stationMOD(coord, map):
    """
        From coordinates, it searches all stations.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """

    possible_origins = []

    min_dist = INF

    for station in range(1, len(map.stations) + 1):
        station_coord = [map.stations[station]["x"], map.stations[station]["y"]]
        station_dist = euclidean_dist(coord, station_coord)
        possible_origins.append([station, station_dist])

    #print(possible_origins)

    return sorted(possible_origins, key=lambda station: station[1]) #Devolvemos todas las estaciones ordenadas por distancia

    pass


def add_ini_dest_cost(llista, dist_origenes, dist_final, walking_distance, map, type_preference=1):
    """
         Calculate the cost from coordinates to initial station and final station to coordinates according to type preference
         Format of the parameter is:
            Args:
                llista (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    ruta_directa = 0  # ruta_directa en adyacencia y transfers tiene un coste 0.
    # Tampoco hace falta updatear .g ya que estos no contarán en el resultado final.

    if type_preference == 1:
        for ruta, initial_dist in zip(llista, dist_origenes):
            ruta.update_g((initial_dist + dist_final)/HUMAN_SPEED)
            # Estamos sumando para ir a la estación y de la final a las coordenadas
        ruta_directa = walking_distance/HUMAN_SPEED

    return llista

    pass


def Astar_improved(origin_coor, dest_coor, map, type_preference=1):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    if type_preference == 1:
        lista_origenes = coord2stationMOD(origin_coor, map)
        lista_destino = coord2station(dest_coor, map)

        origenes = [Path(ori[0]) for ori in lista_origenes] #llista = [origen]
        dist_origenes = [dist[1] for dist in lista_origenes] #Para usar map() falta importar itemgetter
        #  print_list_of_path(origen)
        #  print(dist_origenes)
        destination_id = lista_destino[0]
        TCP = {}  #se supone que esto es un diccionario de costes de las estaciones
        soluciones = Path(destination_id)
        soluciones.g = INF

        dist_final = euclidean_dist(dest_coor, [map.stations[destination_id]['x'], map.stations[destination_id]['y']])
        #xd debería devolver la distancia de la estación destino a las coordenadas finales
        walking_distance = euclidean_dist(origin_coor, dest_coor)
        origenes = add_ini_dest_cost(origenes, dist_origenes, dist_final, walking_distance, map, type_preference)

        for llista in origenes:
            while (origenes) and (origenes[0].last != destination_id):
                C = origenes.pop(0)
                E = expand(C, map)
                E = remove_cycles(E)
                E = calculate_cost(E, map, type_preference)
                E = calculate_heuristics(E, map, destination_id, type_preference)
                remove_redundant_paths(E, origenes, TCP)
                origenes = insert_cost_f(E, origenes)

            if origenes and origenes[0].route[-1] == destination_id:
                if soluciones.g > origenes[0].g:
                    soluciones = origenes.pop(0)
                else:
                    origenes.pop(0)
            else:
                #print("No existeix Solucio")
                pass

        #soluciones.sort(key=lambda path: path.g)
        return soluciones #[0]

    else:
        """Here we found the cases where the type_preference is different from 1.
        Walking is always going to be the best option, because the distance of a straight line will always be lower,
        adjacencies and transfers are cost 0"""

        print("Go by walking, is going to be better.")

    pass