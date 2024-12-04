&rs ∞ &fo "../data/example.txt" # Read file
°□(⊜□ ⊸≠@\n)                    # Split rows, results are boxed
≡(□ ⋕⊜□⊸≠@ °□)                  # Split and parse the rows
≡(□-⇌↘1⇌°□ :↘1°□) .             # Compute deltas
IsOk ← ≡(/× (×≤3:⊸≥1 °□))       # Is this row OK
↥ IsOk ¯ ⟜IsOk                  # Is OK doesn't take into account +-
/+                              # Count OK rows
