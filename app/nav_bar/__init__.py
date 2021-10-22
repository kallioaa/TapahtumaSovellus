from flask_nav.elements import Navbar, View
from flask_nav import Nav

nav = Nav()


@nav.navigation()
def my_nav_bar_text_only():
    return Navbar(
        'Event App'
    )


@nav.navigation()
def my_nav_bar():
    return Navbar(
        'Event App',
        View('Map', "map.map_view"),
        View('Create Event', "new_event.new_event_name"),
    )
