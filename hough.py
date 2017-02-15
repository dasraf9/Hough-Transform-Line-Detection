import cv2
import numpy as np
import sys, getopt


def HoughLines(img,angle,threshold):
	lines = []
	y_idxs, x_idxs = np.nonzero(img)
	thetas = angle*(np.arange(-(np.pi/(angle*2)), (np.pi/(angle*2))))
	cos_t = np.cos(thetas)
	sin_t = np.sin(thetas)
	
	all_lines = {}
	for t in range(len(thetas)):
		for i in range(y_idxs.size):
			r = round(x_idxs[i]*cos_t[t] + y_idxs[i]*sin_t[t])
			if (r,thetas[t]) in all_lines.keys():
				all_lines[(r,thetas[t])] = all_lines[(r,thetas[t])] + 1
			else:
				all_lines[(r,thetas[t])] = 1	
	all_lines = {k:v for (k,v) in all_lines.items() if v >= threshold}
	return np.asarray(list(all_lines.copy().keys()))


def HoughTransform(inputfile,outputfile,cannythreshold):
	src = cv2.imread(inputfile, 1)
	dst = cv2.Canny(src, 50, 200, 3)
	#opencv implementation
	#lines = cv2.HoughLines(dst, 1, (np.pi)/180, 100, 30, 0 )[:,0,:]

	#my implementation
	lines = HoughLines(dst,(np.pi)/180,100)
	#gray to bgr if you want to plot the lines on the detected edges image
	#dst = cv2.cvtColor(dst, 8)

	for line in lines:
		rho = line[0]
		theta = line[1]
		a = np.cos(theta)
		b = np.sin(theta)
		
		x0 = a*rho
		y0 = b*rho
		
		x1 = int(np.round(x0 + 1000*(-b)))
		y1 = int(np.round(y0 + 1000*(a)))
		x2 = int(np.round(x0 - 1000*(-b)))
		y2 = int(np.round(y0 - 1000*(a)))
		
		cv2.line(src,(x1,y1),(x2,y2),(0,255,255), 1)
	
	cv2.imwrite(outputfile,src)
	#cv2.imshow('image',src)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

def main(argv):
	cannythreshold = 50
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('hough.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('hough.py -i <inputfile> -o <outputfile> -c [cannythreshold] ')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-c"):
			cannythreshold = (int)(arg)
	if inputfile == '':
		print('hough.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	if outputfile == '':
		print('hough.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	HoughTransform(inputfile,outputfile,cannythreshold)


if __name__ == "__main__":
   main(sys.argv[1:])