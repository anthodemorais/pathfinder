import collections
import operator

f = open("labyrinth1.txt", "r")
text = f.read()
fullLines = text.split("\n")

lines = [list(x) for x in fullLines]
tree = {}
end = ()
start = ()

for (x, line) in enumerate(lines):
    for (y, col) in enumerate(line):
        validValues = [" ", "X", "@"]
        if col in validValues:
            index = (x, y)
            tree[index] = {}
            if x != 0 and lines[x-1][y] in validValues:
                tree[index][(x-1, y)] = 1
            if x != (len(lines)-1) and lines[x+1][y] in validValues:
                tree[index][(x+1, y)] = 1
            if y != 0 and lines[x][y-1] in validValues:
                tree[index][(x, y-1)] = 1
            if y != (len(line)-1) and lines[x][y+1] in validValues:
                tree[index][(x, y+1)] = 1
            if col == "X":
                end = index
            if col == "@":
                start = index

def getNeighbours(tree, location):
    neighbours = []
    sorted_locations = collections.OrderedDict(tree[location])
    return list(sorted_locations.keys())

def getChildrenPath(tree, location, locations):
    visited = locations
    paths = getNeighbours(tree, location)
    for path in paths:
        if path not in visited:
            visited.append(path)
            getChildrenPath(tree, path, visited)
    return visited

def isReachable(tree, location, target):
    paths = getChildrenPath(tree, location, [])
    return target in paths

# Dijkstra algorithm

# algorithme de Dijkstra : entrées - Graphe, Start, End

# INIT :

# Vérifier que End est reachable depuis Start (sinon erreur)
# Marquer toutes les destinations possibles comme étant à une distance INFINIE (INF)
# Marquer toutes les destinations possibles comme n'ayant pas de prédéacesseur 3bis. Marquer le Start comme étant à une distance 0 !
# PARCOURS DU GRAPHE Pour toutes les destinations possibles : on prend la plus proche : U

# Si U est la destination : on a trouvé !
# Si U n'est pas la destination : On récupère tous ses voisins, et on mets à jour l'annuaire des distance pour les voisins V. Si on met à jour l'annuaire avec une valeur plus petite (distance Start -> V), on remplace, le prédécesseur de V par U. On retire U des destinations possibles et on continue le parcours.
# QUAND ON A TROUVÉ LA DESTINATIONS

# En partant de la destination, on remonte les prédécesseurs.
# => On obtient alors le trajet le plus cours.

def getTrip(graph, start, end):
    if isReachable(graph, start, end):
        destinations = getChildrenPath(graph, start, [])
        times = {}
        predecessors = {}
        visited = []
        for destination in destinations:
            times[destination] = 999999
            predecessors[destination] = None
        times[start] = 0
        nearestCity = visitNearestCity(graph, times, visited)
        while nearestCity != end:
            times, predecessors, visited = tripToChildren(graph, nearestCity, end, times, predecessors, visited)
            nearestCity = visitNearestCity(graph, times, visited)
        predecessor = end
        trip = []
        while predecessor != start:
            trip.append(predecessor)
            predecessor = predecessors[predecessor]
        trip.reverse()
        # return "Path: " + str(trip) + " in: " + str(times[end]) + " steps."
        return trip
    else:
        return "Unreachable"

def tripToChildren(graph, city, end, times, predecessors, visited):
    children = sorted(graph[city].items(), key=lambda kv: kv[1])
    for child in children:
        key, value = child
        if graph[city][key] + times[city] < times[key]:
            predecessors[key] = city
            times[key] = graph[city][key] + times[city]
    visited.append(city)
    return times, predecessors, visited

def visitNearestCity(graph, times, visited):
    children = sorted(times.items(), key=lambda kv: kv[1])
    nearestCity = ()
    counter = 0
    for city, time in children:
        if city not in visited:
            nearestCity = children[counter][0]
            break
        counter += 1
    return nearestCity


path = getTrip(tree, start, end)

for (x, line) in enumerate(lines):
    for (y, col) in enumerate(line):
        if (x, y) in path and col == " ":
            lines[x][y] = "."

finalLines = [''.join(line) for line in lines]
finalPath = "\n".join(finalLines)

print(finalPath)