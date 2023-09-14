with open("file_to_read.txt", "r") as file:
    content = file.read()

terrible_count = content.count("terrible")
terrible_index = 0

new_content = ""
for word in content.split():
    if word == "terrible":
        terrible_index += 1
        if terrible_index % 2 == 0:
            new_content += "pathetic "
        else:
            new_content += "marvellous "
    else:
        new_content += word + " "

with open("result.txt", "w") as file:
    file.write(new_content)

print("the total times the word “terrible” appears is：", terrible_count)