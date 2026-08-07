import heapq

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class SIPP_Node:
    def __init__(self, x, y, is_obstacle=False):
        self.x = x
        self.y = y
        self.is_obstacle = is_obstacle
        
        # Jeśli to regał/ściana, nie ma żadnych bezpiecznych przedziałów
        if self.is_obstacle:
            self.safe_intervals = [] 
        else:
            # Domyślnie: pole jest wolne od t=0 do nieskończoności
            self.safe_intervals = [(0, float('inf'))] 

    def reserve_time(self, start_time, end_time):
        """
        Ta funkcja będzie używana, gdy robot rezerwuje to pole.
        Dzieli ona istniejące przedziały czasowe.
        """
        new_intervals = []
        for interval in self.safe_intervals:
            safe_start, safe_end = interval
            
            # Jeśli rezerwacja całkowicie omija ten przedział, zostawiamy go w spokoju
            if end_time < safe_start or start_time > safe_end:
                new_intervals.append(interval)
            else:
                # Rozbijamy przedział na dwa mniejsze!
                # 1. Okno przed wjazdem robota
                if start_time > safe_start:
                    new_intervals.append((safe_start, start_time - 1))
                # 2. Okno po odjeździe robota
                if end_time < safe_end:
                    new_intervals.append((end_time + 1, safe_end))
                    
        self.safe_intervals = new_intervals
        

class WarehouseMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Generujemy siatkę 2D wypełnioną naszymi inteligentnymi węzłami
        # Używamy list składanych (list comprehension) dla wydajności
        self.grid = [[SIPP_Node(x, y) for y in range(height)] for x in range(width)]
        self.charging_stations = [] # Przechowuje koordynaty (x, y) stacji

    def add_obstacle(self, x, y):
        """
        Zmienia wybrane pole w stałą przeszkodę (np. regał).
        Usuwa dla niego wszelkie bezpieczne przedziały czasowe.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x][y].is_obstacle = True
            self.grid[x][y].safe_intervals = [] 

    def add_charging_station(self, x, y):
        """
        Oznacza pole jako stację ładowania.
        Zauważ, że stacja ładowania domyślnie NIE JEST przeszkodą.
        Robot może przez nią przejechać, jeśli jest akurat pusta.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.charging_stations.append((x, y))

    def get_node(self, x, y):
        """Bezpieczne pobieranie węzła, zapobiega wyjściu poza mapę."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None
    

# 1. Tworzymy magazyn o wymiarach 20x15 metrów (pól)
my_warehouse = WarehouseMap(20, 15)

# 2. Stawiamy regał na środku (np. blokujemy współrzędne od x=5 do x=10 w rzędzie y=7)
for x in range(5, 11):
    my_warehouse.add_obstacle(x, 7)

# 3. Rozstawiamy dwie stacje ładowania w rogach magazynu
my_warehouse.add_charging_station(0, 0)
my_warehouse.add_charging_station(19, 14)





def manhattan_distance(x1, y1, x2, y2):
    """Heurystyka - przewidywany koszt dotarcia do celu."""
    return abs(x1 - x2) + abs(y1 - y2)

def get_earliest_arrival(current_time, neighbor_node):
    """
    Kluczowa funkcja SIPP!
    Sprawdza, czy robot może wjechać na sąsiednie pole.
    Jeśli pole jest zajęte w momencie przyjazdu (current_time + 1),
    szuka najbliższego wolnego okna czasowego.
    """
    arrival_time = current_time + 1 # Zakładamy, że przejazd zajmuje 1 sekundę/jednostkę
    
    for interval_start, interval_end in neighbor_node.safe_intervals:
        # Jeśli przyjeżdżamy w trakcie trwania bezpiecznego okna
        if interval_start <= arrival_time <= interval_end:
            return arrival_time
        # Jeśli przyjeżdżamy za wcześnie, musimy poczekać aż okno się otworzy
        elif arrival_time < interval_start:
            return interval_start 
            
    return None # Brak bezpiecznego okna w przyszłości (pole zablokowane na zawsze)

def find_path_sipp(start_x, start_y, goal_x, goal_y, warehouse, start_time=0):
    """Główny algorytm SIPP dla pojedynczego robota."""
    
    # Kolejka priorytetowa przechowuje krotki:
    # (f_score, g_score (czas), x, y, historia_ścieżki)
    open_set = []
    
    start_h = manhattan_distance(start_x, start_y, goal_x, goal_y)
    heapq.heappush(open_set, (start_h, start_time, start_x, start_y, [(start_x, start_y, start_time)]))
    
    # Odwiedzone stany zapisujemy jako (x, y, id_interwału), 
    # aby nie zapętlić się w tych samych oknach czasowych.
    visited = set()

    while open_set:
        f_score, current_time, x, y, path = heapq.heappop(open_set)

        # Sprawdzamy, czy jesteśmy u celu
        if x == goal_x and y == goal_y:
            return path # Zwracamy gotową listę współrzędnych i czasów!

        # Identyfikator aktualnego przedziału (dla uproszczenia bierzemy sam czas)
        state = (x, y, current_time)
        if state in visited:
            continue
        visited.add(state)

        # Ruchy: Góra, Dół, Lewo, Prawo (oraz opcjonalnie: Czekaj w miejscu)
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = warehouse.get_node(nx, ny)
            
            if neighbor is None or neighbor.is_obstacle:
                continue # Wyszliśmy poza mapę lub trafiliśmy w regał

            # SIPP: Obliczamy, kiedy najwcześniej możemy tam wjechać
            arrival_time = get_earliest_arrival(current_time, neighbor)
            
            if arrival_time is not None:
                # Obliczamy nowe koszty
                new_h = manhattan_distance(nx, ny, goal_x, goal_y)
                new_f = arrival_time + new_h # g_score to tutaj po prostu nasz arrival_time
                
                new_path = list(path)
                new_path.append((nx, ny, arrival_time))
                
                heapq.heappush(open_set, (new_f, arrival_time, nx, ny, new_path))
                
    return None # Nie znaleziono żadnej bezpiecznej ścieżki


class RobotTask:
    def __init__(self, robot_id, start_x, start_y, goal_x, goal_y, priority):
        self.robot_id = robot_id
        self.start_x = start_x
        self.start_y = start_y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.priority = priority # Wyższa wartość = robot jedzie pierwszy!
        self.path = [] # Tu zapiszemy gotową trasę

class FleetManager:
    def __init__(self, warehouse_map):
        self.warehouse = warehouse_map
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def plan_all_paths(self):
        """
        Główne serce systemu. Planuje trasy dla wszystkich robotów
        w kolejności od najwyższego priorytetu.
        """
        # 1. Sortujemy zadania po priorytecie (malejąco)
        self.tasks.sort(key=lambda t: t.priority, reverse=True)
        
        for task in self.tasks:
            print(f"Planowanie trasy: Robot {task.robot_id} (Priorytet: {task.priority})...")
            
            # 2. Szukamy ścieżki algorytmem SIPP (tym z Kroku 3)
            # Domyślnie startujemy w czasie t=0
            path = find_path_sipp(
                task.start_x, task.start_y, 
                task.goal_x, task.goal_y, 
                self.warehouse
            )
            
            if path is None:
                print(f"❌ BŁĄD: Zator! Nie znaleziono trasy dla Robota {task.robot_id}.")
                # Tutaj w przyszłości dodamy mechanizm awaryjnego zjeżdżania na bok
                continue
                
            task.path = path
            print(f"✅ Znaleziono! Trasa składa się z {len(path)} kroków.")
            
            # 3. Magia SIPP: Zapisujemy ślad na mapie!
            self._reserve_path_on_map(path)

    def _reserve_path_on_map(self, path):
        """
        Przechodzi po wyznaczonej ścieżce i usuwa "okna czasowe" z mapy,
        aby kolejne roboty wiedziały, że te pola będą wtedy zajęte.
        """
        for i in range(len(path)):
            x, y, arrival_time = path[i]
            node = self.warehouse.get_node(x, y)
            
            if i < len(path) - 1:
                # Jeśli to nie jest koniec trasy, robot zajmuje pole
                # od momentu wjazdu (arrival_time) do momentu wjazdu na kolejne pole.
                next_time = path[i+1][2]
                node.reserve_time(arrival_time, next_time)
            else:
                # OSTATNI PUNKT: Robot dojechał do celu!
                # Rezerwujemy to pole od momentu przyjazdu do nieskończoności,
                # bo robot tam zostaje (np. przy stacji ładowania).
                node.reserve_time(arrival_time, float('inf'))
                



def visualize_warehouse(fleet_manager):
    warehouse = fleet_manager.warehouse
    
    # 1. Tworzymy "płótno" wykresu
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 2. Rysujemy mapę (siatkę, regały i puste pola)
    for x in range(warehouse.width):
        for y in range(warehouse.height):
            node = warehouse.get_node(x, y)
            if node.is_obstacle:
                # Szary kwadrat z czarną ramką dla regału
                rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='gray')
                ax.add_patch(rect)
            else:
                # Białe tło dla pustego pola (alejki)
                rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=0.5, edgecolor='lightgray', facecolor='white')
                ax.add_patch(rect)

    # 3. Rysujemy stacje ładowania
    for cx, cy in warehouse.charging_stations:
        rect = patches.Rectangle((cx - 0.5, cy - 0.5), 1, 1, linewidth=1, edgecolor='darkgreen', facecolor='lightgreen')
        ax.add_patch(rect)
        # Dodajemy ikonkę/tekst na środku pola
        ax.text(cx, cy, '⚡', ha='center', va='center', fontsize=14)

    # 4. Rysujemy trasy robotów
    # Przygotowujemy paletę kolorów dla różnych robotów
    colors = ['red', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'brown']
    
    for idx, task in enumerate(fleet_manager.tasks):
        if not task.path:
            continue # Pomijamy roboty, które z powodu zatoru nie znalazły trasy
            
        # Wyciągamy same współrzędne X i Y z naszej krotki (x, y, czas)
        path_x = [step[0] for step in task.path]
        path_y = [step[1] for step in task.path]
        
        color = colors[idx % len(colors)]
        
        # Rysujemy ciągłą linię trasy
        ax.plot(path_x, path_y, color=color, linewidth=3, label=f'Robot {task.robot_id} (Priorytet: {task.priority})')
        
        # Oznaczamy punkt STARTOWY (kółko) i KOŃCOWY (gwiazdka)
        ax.plot(task.start_x, task.start_y, marker='o', color=color, markersize=8)
        ax.plot(task.goal_x, task.goal_y, marker='*', color=color, markersize=14)

    # 5. Ustawienia estetyczne wykresu
    ax.set_xlim(-0.5, warehouse.width - 0.5)
    ax.set_ylim(-0.5, warehouse.height - 0.5)
    ax.set_xticks(range(warehouse.width))
    ax.set_yticks(range(warehouse.height))
    ax.set_aspect('equal') # Kwadratowe pola
    ax.set_title("Smart Warehouse - Wizualizacja Tras (Algorytm SIPP)", fontsize=16)
    
    # Wyrzucamy legendę lekko poza wykres, żeby nie zasłaniała mapy
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    
    # Pokazujemy okno z wykresem!
    plt.tight_layout()
    plt.show()
    









def get_position_at_time(path, t):
    """
    Funkcja pomocnicza: Oblicza, gdzie znajduje się robot w danej sekundzie 't'.
    """
    if not path:
        return None
    
    # Jeśli czas jest przed startem lub po dotarciu do celu
    if t <= path[0][2]:
        return path[0][0], path[0][1]
    if t >= path[-1][2]:
        return path[-1][0], path[-1][1]
        
    # Szukamy aktualnej pozycji robota w czasie
    for i in range(len(path) - 1):
        current_step = path[i]
        next_step = path[i+1]
        
        # Jeśli czas 't' jest pomiędzy przyjazdem na obecne pole, a przyjazdem na kolejne
        if current_step[2] <= t < next_step[2]:
            return current_step[0], current_step[1]
            
    return path[-1][0], path[-1][1]

def animate_warehouse(fleet_manager):
    warehouse = fleet_manager.warehouse
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 1. Rysujemy statyczną mapę (identycznie jak w wizualizacji tras)
    for x in range(warehouse.width):
        for y in range(warehouse.height):
            node = warehouse.get_node(x, y)
            if node.is_obstacle:
                rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='gray')
                ax.add_patch(rect)
            else:
                rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=0.5, edgecolor='lightgray', facecolor='white')
                ax.add_patch(rect)

    for cx, cy in warehouse.charging_stations:
        rect = patches.Rectangle((cx - 0.5, cy - 0.5), 1, 1, linewidth=1, edgecolor='darkgreen', facecolor='lightgreen')
        ax.add_patch(rect)
        ax.text(cx, cy, '⚡', ha='center', va='center', fontsize=14)

    # 2. Rysujemy punkty startowe i końcowe (półprzezroczyste)
    colors = ['red', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'brown']
    max_time = 0 # Obliczymy, ile klatek potrzebuje animacja
    
    for idx, task in enumerate(fleet_manager.tasks):
        if not task.path:
            continue
            
        color = colors[idx % len(colors)]
        # Znaczniki startu i celu
        ax.plot(task.start_x, task.start_y, marker='o', color=color, markersize=6, alpha=0.4)
        ax.plot(task.goal_x, task.goal_y, marker='*', color=color, markersize=14, alpha=0.4)
        
        # Znajdujemy najpóźniejszy czas w całym systemie
        if task.path[-1][2] > max_time:
            max_time = task.path[-1][2]

    # Ustawienia wykresu
    ax.set_xlim(-0.5, warehouse.width - 0.5)
    ax.set_ylim(-0.5, warehouse.height - 0.5)
    ax.set_xticks(range(warehouse.width))
    ax.set_yticks(range(warehouse.height))
    ax.set_aspect('equal')
    ax.set_title("Smart Warehouse - Animacja Ruchu", fontsize=16)
    
    # Licznik czasu w rogu ekranu
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=14, fontweight='bold', color='black', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 3. Inicjalizacja "Kropek" (Robotów)
    robot_dots = {}
    for idx, task in enumerate(fleet_manager.tasks):
        if task.path:
            color = colors[idx % len(colors)]
            # Tworzymy puste obiekty linii (punkty), które będziemy przesuwać
            dot, = ax.plot([], [], marker='o', color=color, markersize=16, label=f'Robot {task.robot_id}')
            robot_dots[task.robot_id] = (dot, task.path)

    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    # 4. Funkcja aktualizująca klatki animacji
    def update(frame):
        time_text.set_text(f'Czas: {frame} s')
        
        for robot_id, (dot, path) in robot_dots.items():
            pos = get_position_at_time(path, frame)
            if pos:
                # set_data wymaga list/sekwencji, dlatego pos[0] zamykamy w []
                dot.set_data([pos[0]], [pos[1]])
                
        # Zwracamy wszystkie obiekty, które uległy zmianie
        return [dot for dot, _ in robot_dots.values()] + [time_text]

    # 5. Odpalenie Animacji!
    # interval = 500 oznacza pół sekundy przerwy między klatkami
    # frames = max_time + 3, żeby animacja nie urwała się od razu po dojechaniu
    anim = FuncAnimation(fig, update, frames=max_time + 3, interval=500, blit=False, repeat=False)
    
    plt.tight_layout()
    plt.show()
    





# --- SYMULACJA ---

# 1. Tworzymy mapę 15x10
magazyn = WarehouseMap(15, 10)

# 2. Dodajemy rząd regałów na środku (z "bramą" w połowie)
for x in range(3, 12):
    if x != 7: # Zostawiamy przerwę na przejazd w x=7
        magazyn.add_obstacle(x, 4)
        magazyn.add_obstacle(x, 5)

# 3. Dodajemy stacje ładowania
magazyn.add_charging_station(0, 9)
magazyn.add_charging_station(14, 9)

# 4. Inicjujemy Zarządcę
manager = FleetManager(magazyn)

# 5. Dodajemy zadania (Roboty)
# Robot 1: Jedzie z dołu do stacji ładowania (wysoki priorytet)
manager.add_task(RobotTask(robot_id="R1_Bateria", start_x=1, start_y=1, goal_x=0, goal_y=9, priority=100))

# Robot 2: Przecina magazyn z lewej na prawą (średni priorytet)
manager.add_task(RobotTask(robot_id="R2_Paczka", start_x=0, start_y=2, goal_x=14, goal_y=8, priority=50))

# Robot 3: Jedzie z prawej na lewą przez tę samą "bramę" co R2 (niski priorytet)
manager.add_task(RobotTask(robot_id="R3_Paczka", start_x=13, start_y=1, goal_x=2, goal_y=8, priority=10))

# 6. Odpalamy obliczenia!
manager.plan_all_paths()

# 7. Wyświetlamy wynik
animate_warehouse(manager)