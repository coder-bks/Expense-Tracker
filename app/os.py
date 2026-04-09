import os
group = ["core", "db", "models", "Schemas", "api","crud",]

for g in group:
    os.makedirs(g,exist_ok = True)

