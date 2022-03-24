import os

srcPath = "/home/hooman/ai_framework/server/hs_times_37_3_q20.txt"
destPath = srcPath.replace(".txt", "parsed.txt");


detect_start = {}
detect_stop = {}

decode_start = {}
decode_stop = {}

class_start = {}
class1_stop = {}
class2_stop = {}
class3_stop = {}


# decode_stop,pts:2500000,val:1648082250977050776

in_file = open(srcPath, "r")
src_lines = in_file.readlines()
in_file.close()

for src_line in src_lines:
	# print(src_line)
	if "decode_start" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			decode_start[pts] = val
		except:
			pass

		

	if "decode_stop" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			decode_stop[pts] = val
		except:
			pass


	if "detect_start" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			detect_start[pts] = val
		except:
			pass

	if "detect_stop" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			detect_stop[pts] = val
		except:
			pass


	if "class_start" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			class_start[pts] = val
		except:
			pass

	if "class1_stop" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			class1_stop[pts] = val
		except:
			pass


	if "class2_stop" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			class2_stop[pts] = val
		except:
			pass

	if "class3_stop" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			class3_stop[pts] = val
		except:
			pass





decode_sum = 0
decode_count = 0
decode_max = -1

detect_sum = 0
detect_count = 0
detect_max = -1

class1_sum = 0
class1_count = 0
class1_max = -1

class2_sum = 0
class2_count = 0
class2_max = -1

class3_sum = 0
class3_count = 0
class3_max = -1


out_file = open(destPath,"w")

for pts in detect_start:
	if pts in detect_stop:
		time = detect_stop[pts] - detect_start[pts]
		if time > 0 and time < 10000:
			detect_sum += time
			detect_count += 1
			if time > detect_max:
				detect_max = time
			out_file.write("\ndetect_time: " + str(time) + ", pts: " + str(pts))

for pts in decode_start:
	if pts in decode_stop:
		time = decode_stop[pts] - decode_start[pts]
		if time > 0 and time < 10000:
			decode_sum += time
			decode_count += 1
			if time > decode_max:
				decode_max = time
			out_file.write("\ndecode_time: " + str(time) + ", pts: " + str(pts))

for pts in class_start:
	if pts in class1_stop:
		time = class1_stop[pts] - class_start[pts]
		if time > 0 and time < 10000:
			class1_sum += time
			class1_count += 1
			if time > class1_max:
				class1_max = time
			out_file.write("\nclass1_time: " + str(time) + ", pts: " + str(pts))

for pts in class_start:
	if pts in class2_stop:
		time = class2_stop[pts] - class_start[pts]
		if time > 0 and time < 10000:
			class2_sum += time
			class2_count += 1
			if time > class2_max:
				class2_max = time
			out_file.write("\nclass2_time: " + str(time) + ", pts: " + str(pts))

for pts in class_start:
	if pts in class3_stop:
		time = class3_stop[pts] - class_start[pts]
		if time > 0 and time < 10000:
			class3_sum += time
			class3_count += 1
			if time > class3_max:
				class3_max = time
			out_file.write("\nclass3_time: " + str(time) + ", pts: " + str(pts))

			

out_file.write("\n\n\n\n\n\n")



decode_avg = decode_sum / decode_count
detect_avg = detect_sum / detect_count
class1_avg = class1_sum / class1_count
class2_avg = class2_sum / class2_count
class3_avg = class3_sum / class3_count


out_file.write("\navg_decode: " + str(decode_avg) + ", count: " + str(decode_count))
out_file.write("\navg_detect: " + str(detect_avg) + ", count: " + str(detect_count))
out_file.write("\navg_class1: " + str(class1_avg) + ", count: " + str(class1_count))
out_file.write("\navg_class2: " + str(class2_avg) + ", count: " + str(class2_count))
out_file.write("\navg_class3: " + str(class3_avg) + ", count: " + str(class3_count))

out_file.write("\n\n")
out_file.write("\nmax_decode: " + str(decode_max))
out_file.write("\nmax_detect: " + str(detect_max))
out_file.write("\nmax_class1: " + str(class1_max))
out_file.write("\nmax_class2: " + str(class2_max))
out_file.write("\nmax_class3: " + str(class3_max))

out_file.close()

