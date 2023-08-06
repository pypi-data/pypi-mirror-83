# Copyright 2019-2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Zoom R16 project file library"""

import json
import re

# Frequencies in Hz
MID_FREQ = [
    40,
    50,
    63,
    80,
    100,
    125,
    160,
    200,
    250,
    315,
    400,
    500,
    630,
    800,
    1000,
    1300,
    1600,
    2000,
    2500,
    3200,
    4000,
    5000,
    6300,
    8000,
    10000,
    12500,
    16000,
    18000,
]
HIGH_FREQ = MID_FREQ[11:]
LOW_FREQ = MID_FREQ[:17]

REC = "record"
PLAY = "play"
MUTE = "mute"


class Project:
    """Project on the Zoom R16"""

    file_pattern = r"([A-Z]|[0-9]|_|\-){0,8}.WAV"
    default_name = "PRJ000"
    default_header = "ZOOM R-16  PROJECT DATA VER0001"
    default_bitlength = 16
    default_protected = False
    default_insert_effect_on = True

    def __init__(self, raw=None):
        """A Zoom R16 project.

        :param raw: A byte object representing the entire project file
        content.
        :type raw: byte
        """
        withdefault = raw is None
        if raw is None:
            self.raw = bytearray(3332)
            self._set_default()
        elif isinstance(raw, bytes):
            self.raw = bytearray(raw)
        elif isinstance(raw, bytearray):
            self.raw = raw
        else:
            raise TypeError("Invalid type: %r" % raw)
        self.tracks = [
            Project.Track(index=i, raw=self.raw, withdefault=withdefault)
            for i in range(0, 16)
        ]
        self.master = Project.MasterTrack(
            index=16, raw=self.raw, withdefault=withdefault
        )

    @property
    def header(self):
        """Return header of the project file."""
        return self.raw[0:47].decode(encoding="ascii").strip()

    @header.setter
    def header(self, value):
        """
        Set the header of the project. It's not recommended to change
        the default header of a project. Header max size is 47 ASCII
        characters.
        """
        if not isinstance(value, str):
            raise TypeError(
                "invalid type: get %r expect %r" % type(value), type(str)
            )
        if len(value) > 47:
            raise ValueError(
                "size too long: get %d expect %d" % (len(value), 47)
            )
        # Normalize name to size 47
        value = value.ljust(47)
        try:
            bvalue = value.encode(encoding="ascii")
        except UnicodeEncodeError as err:
            raise ValueError("not an ascii string: " + str(err)) from err
        self.raw[0:47] = bvalue

    @property
    def protected(self):
        """Return True if the project is protected."""
        return bool(self.raw[48])

    @protected.setter
    def protected(self, value):
        """Set the protected bit for the project"""
        self.raw[48] = bool(value)

    @property
    def name(self):
        """Return the name of the project as a string"""
        # Project name 8 bytes long
        return self.raw[52:60].decode(encoding="ascii").strip()

    @name.setter
    def name(self, value):
        """
        Set the name of a project. Name can not be longer than 8
        characters and only ASCII.
        """
        if not isinstance(value, str):
            raise TypeError(
                "invalid type: get %r expect %r" % type(value), type(str)
            )
        if len(value) > 8:
            raise ValueError(
                "size too long: get %d expect %d" % (len(value), 8)
            )
        # Normalize name to size 8
        name = value.ljust(8)
        try:
            bname = name.encode(encoding="ascii")
        except UnicodeEncodeError as err:
            raise ValueError("not an ascii string: " + str(err)) from err
        self.raw[52:60] = bname

    @property
    def bitlength(self):
        """Return bitlength of recorded file. 16bits or 24bits as an int."""
        if self.raw[3320]:
            return 24
        return 16

    @bitlength.setter
    def bitlength(self, value):
        """
        Set the bitlength for the project. The settings will be used
        for all new file recorded with the zoom recorder.
        Bitlength can only take values 16 or 24 (bits).
        """
        if not isinstance(value, int):
            TypeError(
                "invalid type: get %r expect %r" % type(value), type(int)
            )
        if value not in (16, 24):
            raise ValueError(
                "wrong value: get %d expect %d or %d" % (value, 16, 24)
            )
        if value == 24:
            self.raw[3320] = 1
        else:
            self.raw[3320] = 0

    @property
    def insert_effect_on(self):
        """Return True if insert effect is on."""
        length = 4
        pos = 3284
        return bool(
            int.from_bytes(self.raw[pos : pos + length], byteorder="little")
        )

    @insert_effect_on.setter
    def insert_effect_on(self, value):
        """Set insert effect on or off"""
        length = 4
        pos = 3284
        self.raw[pos : pos + length] = int(bool(value)).to_bytes(
            4, byteorder="little"
        )

    def _set_default(self):
        """Set default value to the project."""
        self.header = self.default_header
        self.name = self.default_name
        self.bitlength = self.default_bitlength
        self.protected = self.default_protected
        self.insert_effect_on = self.default_insert_effect_on

    def todict(self):
        """Return a dictionary representing the project"""
        res = {}
        res["header"] = self.header
        res["name"] = self.name
        res["bitlength"] = self.bitlength
        res["protected"] = self.protected
        res["insert_effect_on"] = self.insert_effect_on
        res["tracks"] = [track.todict() for track in self.tracks]
        res["master"] = self.master.todict()
        return res

    def tojson(self, indent=4):
        """Return a json string representing the project"""
        return json.dumps(self.todict(), indent=indent)

    class Track:
        """Track on the Zoom R16"""

        default_file = ""
        default_status = PLAY
        default_stereo_on = False
        default_invert_on = False
        default_pan = 0
        default_fader = 100
        default_chorus_on = True
        default_chorus_gain = 0
        default_reverb_on = True
        default_reverb_gain = 0
        default_eqhigh_on = True
        default_eqhigh_freq = 8000
        default_eqhigh_gain = 0
        default_eqmid_on = True
        default_eqmid_freq = 1000
        default_eqmid_qfactor = 0.5
        default_eqmid_gain = 0
        default_eqlow_on = True
        default_eqlow_freq = 125
        default_eqlow_gain = 0

        def __init__(self, index, raw, withdefault=False):
            self.index = index
            self.raw = raw
            if withdefault:
                self._set_default()

        @property
        def file(self):
            """Name of the file associated with this track"""
            # 12 bytes long + 4 null bytes
            length = 16
            pos = 1192 + self.index * length
            # Check if there is a file attached to this track or not
            is_file = int.from_bytes(
                self.raw[pos : pos + (length - 4)], byteorder="little"
            )
            if is_file:
                return (
                    self.raw[pos : pos + (length - 4)]
                    .decode(encoding="ascii")
                    .strip()
                )
            return ""

        @file.setter
        def file(self, value):
            """
            Set the name of the file associated to a track. Max length is 12
            characters including extension (.WAV), so 8 characters for the
            name of the file.
            Characters can only be :
                - 0-9: Numerals
                - A-Z: ASCII capital letters
                - _ -: Underscore and dash
            12 null bytes means that there is no file attached to this
            track.
            """
            # 12 bytes long + 4 null bytes
            length = 16
            pos = 1192 + self.index * length
            if not isinstance(value, str):
                raise TypeError(
                    "invalid type: get %r expect %r" % (type(value), type(str))
                )
            if len(value) > 12:
                raise ValueError(
                    "size too long: get %d expect %d" % (len(value), 12)
                )
            if value:
                if not re.fullmatch(Project.file_pattern, value):
                    raise ValueError(
                        "filename does not conform to filname rules."
                    )
                # Normalize value to size 12
                value = value.ljust(12)
                bvalue = value.encode(encoding="ascii")
                bvalue = bvalue + bytes(4)
            else:
                bvalue = bytes(16)
            self.raw[pos : pos + length] = bvalue

        @property
        def status(self):
            """Return the status of the track (mute / play / record)"""
            # Status are stored bitwise among 2 bytes in this order
            # 7 6 5 4  3 2 1 0    15 14 13 12  11 10 9 8
            # (numbers are track index)
            length = 2
            pos_rec = 80
            pos_play = 84
            pos_mask = 1 << self.index
            rec_byte_vals = int.from_bytes(
                self.raw[pos_rec : pos_rec + length], byteorder="little"
            )
            play_byte_vals = int.from_bytes(
                self.raw[pos_play : pos_play + length], byteorder="little"
            )
            rec_value = rec_byte_vals & pos_mask
            play_value = play_byte_vals & pos_mask
            if rec_value:
                return REC
            if play_value:
                return PLAY
            return MUTE

        @status.setter
        def status(self, value):
            """
            Set status for a track. Value must be one of the module
            constant REC, PLAY or MUTE.
            """
            if value not in (REC, PLAY, MUTE):
                raise ValueError("wrong value: %r" % value)
            length = 2
            pos_rec = 80
            pos_play = 84
            pos_mask = 1 << self.index
            rec_vals = int.from_bytes(
                self.raw[pos_rec : pos_rec + length], byteorder="little"
            )
            play_vals = int.from_bytes(
                self.raw[pos_play : pos_play + length], byteorder="little"
            )
            # Clear rec and play values for this track
            rec_vals = rec_vals & ~pos_mask
            play_vals = play_vals & ~pos_mask
            if value == REC:
                # Set record bit to 1
                self.raw[pos_rec : pos_rec + length] = (
                    rec_vals | pos_mask
                ).to_bytes(2, byteorder="little")
                # Set play bit to 1
                self.raw[pos_play : pos_play + length] = (
                    play_vals | pos_mask
                ).to_bytes(2, byteorder="little")
            elif value == PLAY:
                # Set play bit to 1
                self.raw[pos_play : pos_play + length] = (
                    play_vals | pos_mask
                ).to_bytes(2, byteorder="little")
            else:
                self.raw[pos_rec : pos_rec + length] = (rec_vals).to_bytes(
                    2, byteorder="little"
                )
                self.raw[pos_play : pos_play + length] = (play_vals).to_bytes(
                    2, byteorder="little"
                )

        @property
        def stereo_on(self):
            """Return True if this track is stereo"""
            # 2 bytes. On bit for each track
            length = 2
            pos = 1184
            pos_mask = 1 << self.index
            byte_vals = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            values = byte_vals & pos_mask
            return bool(values)

        @stereo_on.setter
        def stereo_on(self, value):
            """Set the stereo parameter to true or false"""
            length = 2
            pos = 1184
            pos_mask = 1 << self.index
            stereo_vals = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            # Clear stereo values for this track
            stereo_vals = stereo_vals & ~pos_mask
            if value:
                self.raw[pos : pos + length] = (
                    stereo_vals | pos_mask
                ).to_bytes(2, byteorder="little")
            else:
                self.raw[pos : pos + length] = (stereo_vals).to_bytes(
                    2, byteorder="little"
                )

        @property
        def invert_on(self):
            """Return True if this track is inverted"""
            length = 4
            pos = 352 + self.index * length
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return bool(value)

        @invert_on.setter
        def invert_on(self, value):
            """Set property to inverse phase of the track"""
            length = 4
            pos = 352 + self.index * length
            self.raw[pos : pos + length] = int(bool(value)).to_bytes(
                length, byteorder="little"
            )

        @property
        def pan(self):
            """
            Return pan of this track.
            -50 is totally left and 50 is totally right. 0 means centered.
            """
            # 4 bytes long as an integer between 0-100
            length = 4
            pos = 160 + self.index * length
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value - 50

        @pan.setter
        def pan(self, value):
            """
            Set panoramic equalization of this track.
            value is always rounded to the nearest integer.
            -50 is totally left and 50 is totally right. 0 means centered.
            """
            # Put value from [-50; 50] to [0; 100] interval
            value = round(value) + 50
            value = min(value, 100)
            value = max(0, value)
            # Store value
            length = 4
            pos = 160 + self.index * length
            self.raw[pos : pos + length] = value.to_bytes(
                length, byteorder="little"
            )

        @property
        def fader(self):
            """Return the fader value for this track. Value between 0-127"""
            # 4 bytes long as an integer between 0-127
            length = 4
            pos = 96 + self.index * length
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value

        @fader.setter
        def fader(self, value):
            """Set the fader value for this track. Value between 0-127"""
            value = int(value)  # Do not catch ValueError
            value = min(value, 127)
            value = max(value, 0)
            # 4 bytes long as an integer between 0-127
            length = 4
            pos = 96 + self.index * length
            self.raw[pos : pos + length] = value.to_bytes(
                length, byteorder="little"
            )

        # Effects

        @property
        def chorus_on(self):
            """Return True if chorus is on"""
            # 2 bytes. One bit for each track
            length = 2
            pos = 1468
            pos_mask = 1 << self.index
            byte_vals = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            values = byte_vals & pos_mask
            return bool(values)

        @chorus_on.setter
        def chorus_on(self, value):
            """Set property to enable chorus effect on the track"""
            length = 2
            pos = 1468
            pos_mask = 1 << self.index
            chorus_vals = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            # Clear values for this track
            chorus_vals = chorus_vals & ~pos_mask
            if value:
                self.raw[pos : pos + length] = (
                    chorus_vals | pos_mask
                ).to_bytes(2, byteorder="little")
            else:
                self.raw[pos : pos + length] = (chorus_vals).to_bytes(
                    2, byteorder="little"
                )

        @property
        def chorus_gain(self):
            """
            Return the fader value for the chorus of this track in
            percentage.
            """
            # 4 bytes long as an integer between 0-100
            length = 4
            pos = 224 + self.index * length
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value

        @chorus_gain.setter
        def chorus_gain(self, value):
            """Set the gain of the chorus effect on this track."""
            value = int(value)  # Do not catch ValueError
            value = min(value, 100)
            value = max(value, 0)
            # 4 bytes long as an integer between 0-100
            length = 4
            pos = 224 + self.index * length
            self.raw[pos : pos + length] = value.to_bytes(
                length, byteorder="little"
            )

        @property
        def reverb_on(self):
            """Return True if reverb is on"""
            # 2 bytes. One bit for each track
            length = 2
            pos = 1472
            pos_mask = 1 << self.index
            byte_vals = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            values = byte_vals & pos_mask
            return bool(values)

        @reverb_on.setter
        def reverb_on(self, value):
            """Set property to enable reverb effect on the track"""
            length = 2
            pos = 1472
            pos_mask = 1 << self.index
            reverb_vals = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            # Clear values for this track
            reverb_vals = reverb_vals & ~pos_mask
            if value:
                self.raw[pos : pos + length] = (
                    reverb_vals | pos_mask
                ).to_bytes(2, byteorder="little")
            else:
                self.raw[pos : pos + length] = (reverb_vals).to_bytes(
                    2, byteorder="little"
                )

        @property
        def reverb_gain(self):
            """
            Return the fader value for the reverb of this track in
            percentage.
            """
            # 4 bytes long as an integer between 0-100
            length = 4
            pos = 288 + self.index * length
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value

        @reverb_gain.setter
        def reverb_gain(self, value):
            """Set the gain of the reverb effect on this track."""
            value = int(value)  # Do not catch ValueError
            value = min(value, 100)
            value = max(value, 0)
            # 4 bytes long as an integer between 0-100
            length = 4
            pos = 288 + self.index * length
            self.raw[pos : pos + length] = value.to_bytes(
                length, byteorder="little"
            )

        # Equalizer
        #
        # Each equalizer has 16 bytes to store: on/off (4 bytes), frequency
        # (8 bytes), and fader (4 bytes) in that order.
        # The three equlizer are stored together in this order:
        # 1. Hight EQ (16 bytes)
        # 2. Mid EQ (16 bytes)
        # 3. Low EQ (16 bytes)
        # So, for each track, there is a pack of 3 * 16 = 48 bytes for
        # equalizer settings.
        # Equalizer settings are stored by tracks. So eq for track 1, then
        # eq for track 2, etc. It begins at position 416 (decimal).
        #
        # Details:
        # Track 1
        # 416: eqhigh_on (4 bytes)
        # 420: eqhigh_freq (4 bytes)
        # 424: not used (4 bytes)
        # 428: eqhigh_gain (4 bytes)
        # 432: eqmid_on (4 bytes)
        # 436: eqmid_freq (4 bytes)
        # 440: eqmid_qfactor (4 bytes)
        # 444: eqmid_gain (4 bytes)
        # 448: eqlow_on (4 bytes)
        # 452: eqlow_freq (4 bytes)
        # 456: not used (4 bytes)
        # 460: eqlow_gain (4 bytes)
        # Track 2
        # 464: eqhigh_on (4 bytes)
        # ...

        @property
        def eqhigh_on(self):
            """Return True if the equalizer for high frequency is on"""
            length = 4
            pos = 416 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return bool(value)

        @eqhigh_on.setter
        def eqhigh_on(self, value):
            """Set equalizer for high frequency on or off."""
            length = 4
            pos = 416 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = int(bool(value)).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqhigh_freq(self):
            """
            Return the frequency for the high equalizer.
            Values: in Hz see HIGH_FREQ table.
            """
            length = 4
            pos = 420 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return HIGH_FREQ[value]

        @eqhigh_freq.setter
        def eqhigh_freq(self, value):
            """
            Set frequency for the high equalizer.
            Value must be one of the HIGH_FREQ table.
            """
            if value not in HIGH_FREQ:
                raise ValueError(
                    "wrong value '%s' not found in HIGH_FREQ table" % value
                )
            length = 4
            pos = 420 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = HIGH_FREQ.index(value).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqhigh_gain(self):
            """
            Return the gain of the high frequency equalizer.
            Value between -12 dB and +12 dB.
            Stored as an integer between 0 and 24.
            """
            length = 4
            pos = 428 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value - 12

        @eqhigh_gain.setter
        def eqhigh_gain(self, value):
            """
            Set the gain of the high frequency equalizer.
            Value between -12 and +12 (dB).
            """
            value = int(value)  # Do not catch ValueError
            value = min(value, 12)
            value = max(value, -12)
            length = 4
            pos = 428 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = (value + 12).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqmid_on(self):
            """Return True if the equalizer for mid frequency is on"""
            length = 4
            pos = 432 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return bool(value)

        @eqmid_on.setter
        def eqmid_on(self, value):
            """Set equalizer for mid frequency on or off."""
            length = 4
            pos = 432 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = int(bool(value)).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqmid_freq(self):
            """Return the frequency for the mid equalizer.
            Values: in Hz see MID_FREQ table.
            """
            length = 4
            pos = 436 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return MID_FREQ[value]

        @eqmid_freq.setter
        def eqmid_freq(self, value):
            """
            Set frequency for the medium equalizer.
            Value must be one of the MID_FREQ table.
            """
            if value not in MID_FREQ:
                raise ValueError(
                    "wrong value '%s' not found in MID_FREQ table" % value
                )
            length = 4
            pos = 436 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = MID_FREQ.index(value).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqmid_qfactor(self):
            """
            The q-factor for the mid frequency. Value between 0.1 to 1.0.
            Values are stored as an integer. 0 means a qfactor of 0.1, 1
            means a qfactor of 0.2, etc.
            """
            length = 4
            pos = 440 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            # Rounding to prevent floating computation errors with 0.1
            return round(0.1 * (value + 1), 1)

        @eqmid_qfactor.setter
        def eqmid_qfactor(self, value):
            """
            Set the gain of the medium frequency equalizer.
            Value between 0.1 and 1.0.
            """
            value = float(value)  # Do not catch ValueError
            value = min(value, 1)
            value = max(value, 0.1)
            value = round(value, 1)
            length = 4
            pos = 440 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = int(value * 10 - 1).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqmid_gain(self):
            """
            Return the gain of the mid frequency equializer.
            Value between -12 db and +12 db.
            """
            length = 4
            pos = 444 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value - 12

        @eqmid_gain.setter
        def eqmid_gain(self, value):
            """
            Set the gain of the medium frequency equalizer.
            Value between -12 and +12 (dB).
            """
            value = int(value)  # Do not catch ValueError
            value = min(value, 12)
            value = max(value, -12)
            length = 4
            pos = 444 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = (value + 12).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqlow_on(self):
            """Return True if the equalizer for low frequency is on"""
            length = 4
            pos = 448 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return bool(value)

        @eqlow_on.setter
        def eqlow_on(self, value):
            """Set equalizer for low frequency on or off."""
            length = 4
            pos = 448 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = int(bool(value)).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqlow_freq(self):
            """Return the frequency for the low equalizer.
            Values: in Hz see LOW_FREQ table.
            """
            length = 4
            pos = 452 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return LOW_FREQ[value]

        @eqlow_freq.setter
        def eqlow_freq(self, value):
            """
            Set frequency for the low equalizer.
            Value must be one of the LOW_FREQ table.
            """
            if value not in LOW_FREQ:
                raise ValueError(
                    "wrong value '%s' not found in LOW_FREQ table" % value
                )
            length = 4
            pos = 452 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = LOW_FREQ.index(value).to_bytes(
                4, byteorder="little"
            )

        @property
        def eqlow_gain(self):
            """
            Return the gain of the low frequency equializer.
            Value between -12 db and +12 db.
            """
            length = 4
            pos = 460 + self.index * (3 * 16)  # See note above
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value - 12

        @eqlow_gain.setter
        def eqlow_gain(self, value):
            """
            Set the gain of the low frequency equalizer.
            Value between -12 and +12 (dB).
            """
            value = int(value)  # Do not catch ValueError
            value = min(value, 12)
            value = max(value, -12)
            length = 4
            pos = 460 + self.index * (3 * 16)  # See note above
            self.raw[pos : pos + length] = (value + 12).to_bytes(
                4, byteorder="little"
            )

        def _set_default(self):
            """Set default values for track properties"""
            self.file = self.default_file
            self.status = self.default_status
            self.stereo_on = self.default_stereo_on
            self.invert_on = self.default_invert_on
            self.pan = self.default_pan
            self.fader = self.default_fader
            self.chorus_on = self.default_chorus_on
            self.chorus_gain = self.default_chorus_gain
            self.reverb_on = self.default_reverb_on
            self.reverb_gain = self.default_reverb_gain
            self.eqhigh_on = self.default_eqhigh_on
            self.eqhigh_freq = self.default_eqhigh_freq
            self.eqhigh_gain = self.default_eqhigh_gain
            self.eqmid_on = self.default_eqmid_on
            self.eqmid_freq = self.default_eqmid_freq
            self.eqmid_qfactor = self.default_eqmid_qfactor
            self.eqmid_gain = self.default_eqmid_gain
            self.eqlow_on = self.default_eqlow_on
            self.eqlow_freq = self.default_eqlow_freq
            self.eqlow_gain = self.default_eqlow_gain

        def todict(self):
            """Return a dictionary representing the track"""
            res = {}
            res["file"] = self.file
            res["status"] = self.status
            res["stereo_on"] = self.stereo_on
            res["invert_on"] = self.invert_on
            res["pan"] = self.pan
            res["fader"] = self.fader
            res["chorus_on"] = self.chorus_on
            res["chorus_gain"] = self.chorus_gain
            res["reverb_on"] = self.reverb_on
            res["reverb_gain"] = self.reverb_gain
            res["eqhigh_on"] = self.eqhigh_on
            res["eqhigh_freq"] = self.eqhigh_freq
            res["eqhigh_gain"] = self.eqhigh_gain
            res["eqmid_on"] = self.eqmid_on
            res["eqmid_freq"] = self.eqmid_freq
            res["eqmid_qfactor"] = self.eqmid_qfactor
            res["eqmid_gain"] = self.eqmid_gain
            res["eqlow_on"] = self.eqlow_on
            res["eqlow_freq"] = self.eqlow_freq
            res["eqlow_gain"] = self.eqlow_gain
            return res

    class MasterTrack:
        """Master track on the Zoom R16"""

        default_file = ""
        default_fader = 100

        def __init__(self, index, raw, withdefault=False):
            self.index = index
            self.raw = raw
            if withdefault:
                self._set_default()

        @property
        def file(self):
            """Name of the file associated with this track"""
            # 12 bytes long + 4 null bytes
            # Follow the other tracks name
            length = 16
            pos = 1448  # 1192 + 16 * length
            # Check if there is a file attached to this track or not
            is_file = int.from_bytes(
                self.raw[pos : pos + (length - 4)], byteorder="little"
            )
            if is_file:
                return (
                    self.raw[pos : pos + (length - 4)]
                    .decode(encoding="ascii")
                    .strip()
                )
            return ""

        @file.setter
        def file(self, value):
            """
            Set the name of the file associated to a track. Max length is 12
            characters including extension (.WAV), so 8 characters for the
            name of the file.
            Characters can only be :
                - 0-9: Numerals
                - A-Z: ASCII capital letters
                - _ -: Underscore and dash
            12 null bytes means that there is no file attached to this
            track.
            """
            # 12 bytes long + 4 null bytes
            length = 16
            pos = 1448
            if not isinstance(value, str):
                raise TypeError(
                    "invalid type: get %r expect %r" % (type(value), type(str))
                )
            if len(value) > 12:
                raise ValueError(
                    "size too long: get %d expect %d" % (len(value), 12)
                )
            if value:
                if not re.fullmatch(Project.file_pattern, value):
                    raise ValueError(
                        "filename does not conform to filname rules."
                    )
                # Normalize value to size 12
                value = value.ljust(12)
                bvalue = value.encode(encoding="ascii")
                bvalue = bvalue + bytes(4)
            else:
                bvalue = bytes(16)
            self.raw[pos : pos + length] = bvalue

        @property
        def fader(self):
            """Return the fader value for this track in percentage"""
            length = 4
            pos = 1188
            value = int.from_bytes(
                self.raw[pos : pos + length], byteorder="little"
            )
            return value

        @fader.setter
        def fader(self, value):
            """Set the fader value for this track. Value between 0-127"""
            value = int(value)  # Do not catch ValueError
            value = min(value, 127)
            value = max(value, 0)
            # 4 bytes long as an integer between 0-127
            length = 4
            pos = 1188
            self.raw[pos : pos + length] = value.to_bytes(
                length, byteorder="little"
            )

        def _set_default(self):
            """Set default value to master track."""
            self.file = self.default_file
            self.fader = self.default_fader

        def todict(self):
            """Return a dictionary representing the track"""
            res = {}
            res["file"] = self.file
            res["fader"] = self.fader
            return res
