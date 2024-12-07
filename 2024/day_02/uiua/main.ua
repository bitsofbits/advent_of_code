# Parse
&rs ∞ &fo "../data/data.txt"
°□(⊜□ ⊸≠@\n)
⍚(⋕⊜□⊸≠@ )
. # Make a copy of parsed data on stack for Part 2

# Part 2
ComputeDelta ← - ⍜⇌(↘1) ⟜(↘1)
BaseOk       ← (/× (×≤3⟜(≥1) ComputeDelta))
IsOk         ← ≡◇BaseOk
/+ ↥ IsOk ¯ ⟜IsOk

# Part 2
:
IsOkDrop ← ≡◇(
  /↥ [
    ⍥◌3
    ⍢(⊙(+1)⊙⟜(:BaseOk↻¯:↘1:⟜↻:,)|◡<)
  ] : 0⧻.)
↥ IsOkDrop¯ ⟜IsOkDrop
/+
