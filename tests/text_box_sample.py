from termutils import TextBox, Term
import threading
import time

term = Term()
term.clear(flush=True)
term.cursor_hide(flush=True)
text_box_1 = TextBox(0, 0, -5, -10)
text_box_2 = TextBox(0, -10, -5, -1, background="red", foreground="blue")
text_box_3 = TextBox(-5, 0, -1, -10, background="green", foreground="black")
text_box_4 = TextBox(-5, -10, -1, -1, background="yellow", foreground="black")
text = """
"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam,
eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam
voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione
voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci
velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut
enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi
consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur,
vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
"""
text = text.strip()
text_2 = text[:2]
text_3 = text[:2]
lowest_sleep = 0.01
highest_sleep = 0.3
exponent = 0.1
N = 5


def text_box_anim(text_box, text, lowest_sleep, highest_sleep, exponent):
    text_box.run()
    text_len = len(text.strip().split("\n")[0])
    coeff = (lowest_sleep - highest_sleep) / ((text_len + 1) ** exponent)
    text_box(text)
    while True:
        for i in range(-text_len - 1, text_len + 1):
            text_box.set_view(0, i)
            time.sleep(coeff * abs(i) ** exponent + highest_sleep)


thread1 = threading.Thread(
    target=text_box_anim,
    args=(
        text_box_1,
        text,
        0.01,
        0.3,
        0.1,
    ),
    daemon=True,
)
thread2 = threading.Thread(
    target=text_box_anim,
    args=(
        text_box_2,
        text,
        0.05,
        0.05,
        0.01,
    ),
    daemon=True,
)
thread3 = threading.Thread(
    target=text_box_anim,
    args=(
        text_box_3,
        text,
        0.001,
        0.1,
        0.9,
    ),
    daemon=True,
)
thread4 = threading.Thread(
    target=text_box_anim,
    args=(
        text_box_4,
        text,
        0.1,
        0.1,
        0.1,
    ),
    daemon=True,
)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

time.sleep(25)
term.clear(flush=True)
term.cursor_show(flush=True)
