import os

srcPath = "/home/hooman/ai_framework/server/hs_times_37_5_q20.txt"
destPath = srcPath.replace(".txt", "parsed.txt");


batcher_frame_recieved = {}
detect_start = {}
detect_stop = {}

decode_start = {}
decode_stop = {}

class_start = {}
class1_stop = {}
class2_stop = {}
class3_stop = {}

batcher_frame_recieved_pts = {}
batcher_frame_recieved = {}
batch_sent = {}
detect_frame_received_ = {}

# decode_stop,pts:2500000,val:1648082250977050776

in_file = open(srcPath, "r")
src_lines = in_file.readlines()
in_file.close()

for src_line in src_lines:
	# print(src_line)


	if "batcher_frame_recieved" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			batch = int(sp[3].split(":")[-1])
			batcher_frame_recieved_pts[pts] = val
			batcher_frame_recieved[batch] = val
		except:
			pass

	if "batch_sent" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			# val = int(sp[2].split(":")[-1])
			batch = int(sp[3].split(":")[-1])
			batch_sent[batch] = val
		except:
			pass

	if "detect_frame_received_" in src_line:
		sp = src_line.split(",")
		try:
			pts = int(sp[1].split(":")[-1])
			val = int(sp[2].split(":")[-1])
			detect_frame_received_[pts] = val
		except:
			pass



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



frame_batching_sum = 0
frame_batching_count = 0
frame_batching_max = 0

frame_batch_send_sum = 0
frame_batch_send_count = 0
frame_batch_send_max = 0

detector_batching_sum = 0
detector_batching_count = 0
detector_batching_max = 0



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

for batch_nb in batcher_frame_recieved:
	if batch_nb in batch_sent:
		time = batch_sent[batch_nb] - batcher_frame_recieved[batch_nb]
		if time > 0 and time < 10000:
			frame_batching_sum += time
			frame_batching_count += 1
			if time > frame_batching_max:
				frame_batching_max = time
			out_file.write("\nframe_batching_time: " + str(time) + ", batch_nb: " + str(batch_nb))


for pts in batcher_frame_recieved_pts:
	if pts in detect_frame_received_:
		time = detect_frame_received_[pts] - batcher_frame_recieved_pts[pts]
		if time > 0 and time < 10000:
			frame_batch_send_sum += time
			frame_batch_send_count += 1
			if time > frame_batch_send_max:
				frame_batch_send_max = time
			out_file.write("\nframe_batch_send_time: " + str(time) + ", pts: " + str(pts))



for pts in detect_frame_received_:
	if pts in detect_start:
		time = detect_start[pts] - detect_frame_received_[pts]
		if time > 0 and time < 10000:
			detector_batching_sum += time
			detector_batching_count += 1
			if time > detector_batching_max:
				detector_batching_max = time
			out_file.write("\ndetector_batching_time: " + str(time) + ", pts: " + str(pts))




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


frame_batching_avg = frame_batching_sum / frame_batching_count
frame_batch_send_avg = frame_batch_send_sum / frame_batch_send_count
detector_batching_avg = detector_batching_sum / detector_batching_count

decode_avg = decode_sum / decode_count
detect_avg = detect_sum / detect_count
class1_avg = class1_sum / class1_count
class2_avg = class2_sum / class2_count
class3_avg = class3_sum / class3_count


out_file.write("\navg_decode: " + str(decode_avg) + ", count: " + str(decode_count))
out_file.write("\nframe_batching_avg: " + str(frame_batching_avg) + ", count: " + str(frame_batching_count))
out_file.write("\nframe_batch_send_avg: " + str(frame_batch_send_avg) + ", count: " + str(frame_batch_send_count))
out_file.write("\ndetector_batching_avg: " + str(detector_batching_avg) + ", count: " + str(detector_batching_count))
out_file.write("\navg_detect: " + str(detect_avg) + ", count: " + str(detect_count))
out_file.write("\navg_class1: " + str(class1_avg) + ", count: " + str(class1_count))
out_file.write("\navg_class2: " + str(class2_avg) + ", count: " + str(class2_count))
out_file.write("\navg_class3: " + str(class3_avg) + ", count: " + str(class3_count))

out_file.write("\n\n")
out_file.write("\nmax_decode: " + str(decode_max))
out_file.write("\nframe_batching_max: " + str(frame_batching_max))
out_file.write("\nframe_batch_send_avg: " + str(frame_batch_send_max))
out_file.write("\ndetector_batching_avg: " + str(detector_batching_max))
out_file.write("\nmax_detect: " + str(detect_max))
out_file.write("\nmax_class1: " + str(class1_max))
out_file.write("\nmax_class2: " + str(class2_max))
out_file.write("\nmax_class3: " + str(class3_max))

out_file.close()

