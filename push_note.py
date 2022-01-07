from pushbullet import Pushbullet
from CONFIG import PUSH_NOT_TOKEN

pd = Pushbullet(PUSH_NOT_TOKEN)


def push_note_(title, body):
    pd.push_note(title, body)


def send_msg(signal, strategy, time_fr, sym, last_close, status):
    header = f'''MARKET ORDER:'''
    msg = f'''signal: {signal}\nstrategy type: {strategy}\ntime frame: {time_fr}\nsymbol: {sym}\nlast close: \
    ${last_close}\nstatus: {status}'''
    push_note_(header, msg)
