import gevent.monkey

gevent.monkey.patch_all()
import gevent
import time
import krpc

from d import launch

conn = krpc.connect(name='User Interface Example')
vessel = conn.space_center.active_vessel

canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (200, 100)
rect.position = (110 - (screen_size[0] / 2), 0)

# Add a button to set the throttle to maximum
button = panel.add_button("Launch")

# Add some text displaying the total engine thrust
text = panel.add_text("Thrust: 0 kN")
text.rect_transform.position = (-5, -30)
text.color = (1, 1, 1)
text.size = 18

# Set up a stream to monitor the throttle button
button_clicked = conn.add_stream(getattr, button, 'clicked')

while True:
    # Handle the throttle button being clicked
    if button_clicked():
        gevent.spawn(launch)
        button.clicked = False

    # Update the thrust text
    text.content = 'Thrust: %d kN' % (vessel.thrust / 1000)

    time.sleep(0.1)
