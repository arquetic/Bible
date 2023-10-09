import json

with open('Vulgata-toTrain.json', 'r', encoding='utf-8') as file:
    data = file.read()

objetos = json.loads(data)

objetos_filtrados = []
texto_fusionado = ""

# Patch process
for objeto in objetos:
    if objeto.get("verse_number").isdigit():
        if texto_fusionado:
            # Merge the accumulated text with the previous valid object
            objetos_filtrados[-1]["verse"] += texto_fusionado

        # Reset merged text
        texto_fusionado = ""

        # Add the current valid object to the result
        objetos_filtrados.append(objeto)
    else:
        # Merge the "verse" property of invalid objects
        texto_fusionado += " " + objeto["verse"]

    # Merge the accumulated text with the last valid object
    if texto_fusionado and objeto == objetos[-1]:
        objetos_filtrados[-1]["verse"] += texto_fusionado

# Save result
with open('Vulgata-toTrain-patched.json', 'w', encoding='utf-8') as file:
    json.dump(objetos_filtrados, file, indent=2, ensure_ascii=False)
