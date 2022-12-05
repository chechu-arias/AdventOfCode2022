
caloric_elements = dict()
with open("input_d1.txt", "r") as f:
    index = 1
    elph_calories = 0
    elph_calories_list = list()
    for line in f:
        if line == "\n":
            caloric_elements[index] = {
                "calories": elph_calories,
                "calories_list": elph_calories_list
            }
            index += 1
            elph_calories = 0
            elph_calories_list = list()
        else:
            v = int(line.replace("\n", ""))
            elph_calories += v
            elph_calories_list.append(v)

print(caloric_elements)

sorted_caloric_elements = sorted(caloric_elements.items(), key=lambda item: item[1]["calories"], reverse=True)

print(f"The elf with most calories has {sorted_caloric_elements[0][1]['calories']}")

top_three = 0
for i in range(3):
    top_three += sorted_caloric_elements[i][1]['calories']

print(f"The top three elves have {top_three} in total.")
