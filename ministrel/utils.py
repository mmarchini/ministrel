import hashlib
from datetime import datetime

from mingus.midi.pyfluidsynth import cfunc, c_void_p, c_int, c_char_p
from mingus.midi.pyfluidsynth import new_fluid_settings, fluid_settings_setstr
from mingus.midi.pyfluidsynth import fluid_synth_sfload, fluid_settings_setint
from mingus.midi.pyfluidsynth import delete_fluid_synth, delete_fluid_settings
from mingus.midi.pyfluidsynth import new_fluid_synth


new_fluid_player = cfunc('new_fluid_player', c_void_p, ('synth', c_void_p, 1))

fluid_player_add = cfunc('fluid_player_add', c_int, ('player', c_void_p, 1),
                         ('midifile', c_char_p, 1))

fluid_player_play = cfunc('fluid_player_play', c_int, ('player', c_void_p, 1))

fluid_player_join = cfunc('fluid_player_join', c_int, ('player', c_void_p, 1))

delete_fluid_player = cfunc('delete_fluid_player', c_int,
                            ('player', c_void_p, 1))

new_fluid_file_renderer = cfunc('new_fluid_file_renderer', c_void_p,
                                ('synth', c_void_p, 1))

delete_fluid_file_renderer = cfunc('delete_fluid_file_renderer', None,
                                   ('dev', c_void_p, 1))

delete_fluid_file_renderer = cfunc('delete_fluid_file_renderer', None,
                                   ('dev', c_void_p, 1))

fluid_player_get_status = cfunc('fluid_player_get_status', c_int,
                                ('player', c_void_p, 1))

fluid_file_renderer_process_block = cfunc('fluid_file_renderer_process_block',
                                          c_int, ('dev', c_void_p, 1))


def fast_render_loop(settings, synth, player):
    FLUID_PLAYER_PLAYING = 1

    renderer = new_fluid_file_renderer(synth)
    if not renderer:
        return

    while (fluid_player_get_status(player) == FLUID_PLAYER_PLAYING):
        if (fluid_file_renderer_process_block(renderer) != 0):
            break

    delete_fluid_file_renderer(renderer)


def play(midifile, sffile, output_filename):
    settings = new_fluid_settings()
    fluid_settings_setstr(settings, 'audio.driver', 'alsa')
    fluid_settings_setstr(settings, 'synth.verbose', 'no')
    fluid_settings_setstr(settings, 'midi.driver', 'alsa_seq')
    fluid_settings_setstr(settings, 'audio.file.name', output_filename)
    fluid_settings_setstr(settings, "player.timing-source", "sample")
    fluid_settings_setint(settings, "synth.parallel-render", 1)

    synth = new_fluid_synth(settings)
    player = new_fluid_player(synth)

    fluid_synth_sfload(synth, sffile, 1)

    fluid_player_add(player, midifile)
    fluid_player_play(player)

    fast_render_loop(settings, synth, player)

    delete_fluid_player(player)
    delete_fluid_synth(synth)
    delete_fluid_settings(settings)


def get_hash():
    hasher = hashlib.sha1()
    hasher.update(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    return hasher.hexdigest()
