class Maybe:
    def __init__(self, valor):
        self.valor = valor

    def bind(self, func):  # Função de alta ordem
        if self.valor is not None:
            return func(self.valor)  # Função de continuação
        else:
            return Maybe(None)  # Monad

    @staticmethod
    def unit(valor):
        return Maybe(valor)  # Monad

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        if task_id < len(self.tasks):
            del self.tasks[task_id]
            return Maybe.unit(True)  # Monad
        else:
            return Maybe.unit(None)  # Monad

    def list_tasks(self):
        return self.tasks

    def sort_tasks_by_priority(self):
        # Função lambda utilizada aqui para classificar as tarefas por prioridade
        self.tasks.sort(key=lambda task: task['priority'])  # Função lambda

def continuation_menu(manager):
    while True:
        print("\n1. Add Task")
        print("2. Remove Task")
        print("3. List Tasks")
        print("4. Sort Tasks by Priority")
        print("5. Exit")

        choice = int(input("Choose an option: "))

        if choice == 1:
            task_name = input("Enter task name: ")
            priority = int(input("Enter priority (1-5): "))
            manager.add_task({'name': task_name, 'priority': priority})
        elif choice == 2:
            task_id = int(input("Enter task id to remove: "))
            # Closure utilizada aqui para manter o estado das tarefas em um contexto
            result = manager.remove_task(task_id)  # Closure
            if result.valor is None:
                print("Task does not exist.")
            else:
                print("Task removed successfully.")
        elif choice == 3:
            tasks = manager.list_tasks()
            # List comprehension utilizada aqui para formatar a exibição das tarefas
            formatted_tasks = [f"Task: {task['name']}, Priority: {task['priority']}" for task in tasks]  # List comprehension
            print("\n".join(formatted_tasks))
        elif choice == 4:
            manager.sort_tasks_by_priority()
            print("Tasks sorted by priority.")
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

def main():
    manager = TaskManager()
    # Função de continuação utilizada para permitir que o usuário escolha entre diferentes operações após realizar uma ação
    continuation_menu(manager)  # Função de continuação

if __name__ == "__main__":
    main()
