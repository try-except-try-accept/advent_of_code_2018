f = open("template.py")
template = f.read()
f.close()

day = input("Enter day :")

with open(f"day{day}a.py", "w") as f:
     f.write(template.replace("DAY = 1", f"DAY = {day}"))

print("Prepared template")

     
