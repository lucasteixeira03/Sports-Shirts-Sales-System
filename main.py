import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from view.menu_view import JanelaPrincipal


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()
