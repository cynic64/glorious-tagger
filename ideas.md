OK, so I want to be able to be able to flag things very quickly.

For starters, I want to go through every song and be able to assign any tag I want.

# Assigning tags
- How to assign a tag? Either by overwriting the old one or adding it.
- Adding it is easy: `echo key: value >> song`
- Changing it is more difficult, I think sed is the way to go
  - Example: `sed -i 's/quality: .*/quality: 3/' song`

Tags:

- Quality
- Chord complexity
- Structural complexity
- Genre
