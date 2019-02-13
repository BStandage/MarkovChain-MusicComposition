from mido import MidiFile
import itertools

'''
1) Check if a note is played at the same time:
- if yes, then add the note to the current "chord"
2) if no, then permute all possible transitions from each note in the previous state to each note in the current state
- Add each combination to the markov chain. With transitions being represented by the each note in the previous state
transitioning to a note in the current state *with a specific duration*

'''

#begins as an empty dictionary
mc = {}

def parse(filename):
    midi = MidiFile(filename)

    current_state = []
    prev_state = []

    for track in midi.tracks:
        for message in track:
            if message.type == "set_tempo":
                tempo = message.tempo
            elif message.type == "note_on":
                print(message)
                # note is played at the same time
                if message.time == 0:
                    current_state.append(message.note)
                # if the note is not played at the same time, then it is the next state from the previous state
                # This means we must permute all possible transitions from notes in the previous state to notes
                # in the current state and add them to the markov chain
                else:
                    permute_transitions(prev_state, current_state, message.time, tempo, midi.ticks_per_beat)
                    prev_state = current_state
                    current_state = []



def permute_transitions(prev_state, current_state, ticks, tempo, tpb):
    for x in list(itertools.product(prev_state, current_state)):
        # add x[0]:{(x[1], time)} to the Markov Chain
        if x[0] not in mc:
            mc[x[0]] = {}
            mc[x[0]][x[1]] = duration(ticks, tempo, tpb)
        else:
            mc[x[0]][x[1]] = duration(ticks, tempo, tpb)



def duration(ticks, tempo, tpb):
    ms = (ticks / tpb * tempo) / 1000
    return int(ms - (ms % 250) + 250)




if __name__ == '__main__':
    parse('bachcontra1.mid')
    #permute_transitions(['a','b','c'], ['a', 'b'], 10, 10, 10)
    print(mc)