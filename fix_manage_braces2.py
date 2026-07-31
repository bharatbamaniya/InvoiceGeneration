import re

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'r') as f:
    lines = f.readlines()

# Look around line 166 (Card ending)
# 166:                    }
# 167:                }
# 168:                }
# 169:            }
# 170:        }

lines[166] = "                    }\n                })\n            }\n"
lines[167] = ""
lines[168] = ""
lines[169] = ""
lines[170] = "        }\n"

with open('app/src/main/java/com/example/ui/screens/ManageItemsScreen.kt', 'w') as f:
    f.writelines(lines)

