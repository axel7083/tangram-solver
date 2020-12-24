import threading
from queue import Queue
from src.scripts import utils
from src.scripts.TangramSolver import TangramSolver
from tkinter import messagebox
from shapely.geos import TopologicalError

running = True


def close_event():
    global running
    running = False


def solve(original, types, window, progress):
    queue = Queue()

    thread = threading.Thread(target=run_in_other_thread,
                              args=(queue, original, types))

    thread.daemon = True  # so you can quit the demo program easily :)
    thread.start()

    window.protocol("WM_DELETE_WINDOW", close_event)
    progress.config(mode="indeterminate", maximum=100, value=0)
    progress.start(10)

    while running:
        if not queue.empty():
            is_success = queue.get()

            if is_success:
                shapes = queue.get()
                final_shapes = queue.get()
                coordinates = queue.get()
                utils.draw_node(shapes, final_shapes, coordinates)
            else:
                messagebox.showerror("Error detected", "It seems that this geometry cannot be solved.")

            progress.stop()
            return True

        window.update()

    window.destroy()
    return False


def run_in_other_thread(queue, original, types):
    tangram_solver = TangramSolver(original, types)

    try:
        shapes, final_shapes, coordinates = tangram_solver.execute()

        queue.put(True)
        queue.put(shapes)
        queue.put(final_shapes)
        queue.put(coordinates)
    except (RuntimeError, TypeError, NameError):
        print("Error: " + str(NameError))
        queue.put(False)
    except TopologicalError:
        print("Error: " + str(TopologicalError))
        queue.put(False)
