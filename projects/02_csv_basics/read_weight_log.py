from pathlib import Path

project_dir = Path(__file__).resolve().parent

private_path = project_dir / "data" / "private" / "weight_log.csv"
sample_path = project_dir / "data" / "sample" / "weight_log.csv"

if private_path.exists():
    data_path = private_path
else:
    data_path = sample_path

with data_path.open(encoding="utf-8") as file:
    content = file.read()

print("Источник данных:", data_path)

lines = content.splitlines()

data_lines = lines[1:]

weights = []
for line in data_lines:
    date_text, weight_text = line.split(",")
    weight = float(weight_text)
    weights.append(weight)
    print("Дата:", date_text, "Вес:", weight)

print("Количество весов:", len(weights))
print("Первый вес:", weights[0])
print("Последний вес:", weights[-1])
weight_change = weights[-1] - weights[0]
rounded_change = round(weight_change, 1)
print("Изменение веса:", rounded_change, "кг")
