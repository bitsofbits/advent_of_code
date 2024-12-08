┌─╴PartOne
  Load ← regex "mul\\((\\d*),(\\d*)\\)" &rs ∞ &fo
  Call ← /+≡/× ⋕ ⍜⍉(↘1) Load
└─╴

┌─╴PartTwo
  Load  ← ⬚"0"regex "((mul)\\((\\d*),(\\d*)\\))|(do\\(\\))|(don\\'t\\(\\))" &rs ∞ &fo
  Start ← ≡(>1⧻ °□) ⍜⍉(°¤↙ 1 ↘ 5)
  Stop  ← ≡(>1⧻ °□) ⍜⍉(°¤↙ 1 ↘ 6)
  Prod  ← ≡/× ⋕ ⍜⍉(↙ 2↘3)
  Mask  ← +1\(↥(¯1)↧0+)-⊃Stop Start
  Call  ← /+×⊃Mask Prod Load
└─╴

PartOne "../data/data.txt"
PartTwo "../data/data.txt"
