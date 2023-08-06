Functions for decomposing nonnegative integers according to various unit scales
and also parsing support for values written in scales.

*Latest release 20201025*:
transcribe: use str(count_i), not str(count) if count == count_i.

Presupplied scales:
* `BINARY_BYTES_SCALE`: Binary units of (B)ytes, KiB, MiB, GiB etc.
* `DECIMAL_BYTES_SCALE`: Decimal units of (B)ytes, KB, MB, GB etc.
* `DECIMAL_SCALE`: Unit suffixes K, M, G etc.
* `TIME_SCALE`: Units of (s)econds, (m)inutes, (h)ours, (d)ays and (w)eeks.
* `UNSCALED_SCALE`: no units

## Function `combine(components, scale)`

Combine a sequence of value components as from `human()` into an integer.

## Function `geek_bytes(n)`

Decompose a nonnegative integer `n` into counts by unit
from `BINARY_BYTES_SCALE`.

## Function `human(n, scale)`

Decompose a nonnegative integer `n` into counts by unit from `scale`.

Parameters:
* `n`: a nonnegative integer.
* `scale`: a sequence of `(factor,unit)` where factor is the
  size factor to the following scale item
  and `unit` is the designator of the unit.

## Function `human_bytes(n)`

Decompose a nonnegative integer `n` into counts by unit
from `DECIMAL_BYTES_SCALE`.

## Function `human_time(n, scale=None)`

Decompose a nonnegative integer `n` into counts by unit
from `TIME_SCALE`.

## Function `multiparse(s, scales, offset=0)`

Parse an integer followed by an optional scale and return computed value.
Returns the parsed value and the new offset.

Parameters:
* `s`: the string to parse.
* `scales`: an iterable of scale arrays of (factor, unit_name).
* `offset`: starting position for parse.

## Function `parse(s, scale, offset=0)`

Parse an integer followed by an optional scale and return computed value.
Returns the parsed value and the new offset.

Parameters:
* `s`: the string to parse.
* `scale`: a scale array of (factor, unit_name).
* `offset`: starting position for parse.

## Function `transcribe(n, scale, max_parts=None, skip_zero=False, sep='')`

Transcribe a nonnegative integer `n` against `scale`.

Parameters:
* `n`: a nonnegative integer.
* `scale`: a sequence of (factor, unit) where factor is the
  size factor to the follow scale and `unit` is the designator
  of the unit.
* `max_parts`: the maximum number of components to transcribe.
* `skip_zero`: omit components of value 0.
* `sep`: separator between words, default: `''`.

## Function `transcribe_bytes_geek(n, max_parts=1, **kw)`

Transcribe a nonnegative integer `n` against `BINARY_BYTES_SCALE`.

## Function `transcribe_bytes_human(n, max_parts=1, **kw)`

Transcribe a nonnegative integer `n` against `DECIMAL_BYTES_SCALE`.

## Function `transcribe_time(n, max_parts=3, **kw)`

Transcribe a nonnegative integer `n` against `TIME_SCALE`.

# Release Log



*Release 20201025*:
transcribe: use str(count_i), not str(count) if count == count_i.

*Release 20200718*:
Use str.isalpha to recognise "unit" words instead of string.ascii_letters (uses new cs.lex.get_chars "callable gochars" mode).

*Release 20200626*:
transcribe: use "%.1f" to format the count if it is not == int(count) ==> a float-with-fraction.

*Release 20200613*:
New UNSCALED_SCALE for no units.

*Release 20190220*:
Dependency fix.

*Release 20181228*:
Initial PyPI release.
