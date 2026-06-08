from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def atualizar(self, produto) -> None:
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def adicionar_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remover_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar_observers(self) -> None:  # Pluralizado para alinhar com o diagrama
        for observer in self._observers:
            observer.atualizar(self) # Passa o próprio objeto (Produto) para o observer