
import numpy as np
import glob
import h5py
import pickle



def pft():
	import multiprocessing
	import pyfftw

	nthreads = multiprocessing.cpu_count()
	#nthreads=1
	print(nthreads)
	pyfftw.config.NUM_THREADS = nthreads
	from threading import Lock
	fourier_lock = Lock()


	ff = pyfftw.interfaces.numpy_fft
	pyfftw.interfaces.cache.enable()

	nx = 4096
	ny = nx#8
	cx = nx//2
	cy = ny//2

	e=np.zeros((nx,ny), np.float32 )

	for j in range(ny):
		for i in range(nx):
			r=np.sqrt((i-cx-1)**2+(j-cy+2)**2)
			if(r<1.1):
				#print(i,j,r)
				e[i,j]=np.sqrt((i-cx)**2+(j-cy)**2)

	#for j in range(ny):  print(e[:,j])

	n = e.ndim
	s = np.shape(e)

	for i in range(1,nx,2):  e[i,:] *= -1


	#    for j in range(ny):
	#        e[i,j] = -e[i,j]

	fourier_lock.acquire()
	f=ff.rfftn(e,axes=(-2,-1), threads=nthreads)
	fourier_lock.release()
	#f
	fourier_lock.acquire()
	o=ff.irfftn(f,axes=(-2,-1), threads=nthreads)
	fourier_lock.release()
	for i in range(1,nx,2):  o[i,:] *= -1
	#for j in range(ny):  print(o[:,j])
	#o=ff.ifftn(f,axes=(-2,-1)).real

	print("DONE")



def get_smv_header(image_file):
    with open(image_file, "rb") as fh:
        header_info = fh.read(45).decode("ascii", "ignore")
        header_size = int( header_info.split("\n")[1].split("=")[1].replace(";", "").strip() )
        fh.seek(0)
        header_text = fh.read(header_size).decode("ascii", "ignore")
    header_dict = {}
    for record in header_text.split("\n"):
        if record == "}":
            break
        if "=" not in record:
            continue
        key, value = record.replace(";", "").split("=")
        header_dict[key.strip()] = value.strip()
    return header_size, header_dict

def get_smv_data(image_file):
    with open(image_file, "rb") as fh:
        header_info = fh.read(45).decode("ascii", "ignore")
        header_size = int( header_info.split("\n")[1].split("=")[1].replace(";", "").strip() )
        fh.seek(0)
        header_text = fh.read(header_size).decode("ascii", "ignore")
        header_dict = {}
        for record in header_text.split("\n"):
            if record == "}":
                break
            if "=" not in record:
                continue
            key, value = record.replace(";", "").split("=")
            header_dict[key.strip()] = value.strip()
        size1 = int(header_dict['SIZE1'])
        size2 = int(header_dict['SIZE2'])
        data = np.fromfile(fh, dtype=np.uint16, count=size1 * size2)
        data = np.reshape(data,(size1,size2))
    return header_dict, data

def read_image(wildcardPathStr):
    file_list1 = glob.glob(wildcardPathStr)
    file_list2 = sorted(file_list1)
    if len(file_list2) > 1:
        img_list = []
        for f in file_list2:
            img = EDdata(f)
            img_list.append(img)
        return img_list
    if len(file_list2) == 1:
        f = file_list2[0]
        img = EDdata(f)
        return img

def write_image(imgData, filePathStr):
    if type(imgData) is list:
        for img in imgData:
            img.addImage(filePathStr)
    else:
        imgData.addImage(filePathStr)

class EDdata:
    def __init__(self, filePathStr = None):
        if filePathStr is None:
            pass
        else:
            header_dict, data = get_smv_data(filePathStr)
            self.data = data
            self.header_dict = header_dict
 
    def addImage(self, filePathStr):
        with h5py.File(filePathStr, 'a') as f:
            if "/MDF/images" in f:
                g2 = f['/MDF/images']
                imageid_max = g2.attrs['imageid_max']
                imageid_max[0] += 1
                g2.attrs['imageid_max'] = imageid_max
                g1 = f.create_group('/MDF/images/' + str(imageid_max[0]))
                g1.attrs['EMAN.apix_x'] = np.array([1.0],dtype='f')
                g1.attrs['EMAN.apix_y'] = np.array([1.0],dtype='f')
                g1.attrs['EMAN.apix_z'] = np.array([1.0],dtype='f')
                g1.attrs['EMAN.nx'] = np.array([self.data.shape[0]])
                g1.attrs['EMAN.ny'] = np.array([self.data.shape[1]])
                g1.attrs['EMAN.nz'] = np.array([1])
                g1.create_dataset('image', data = self.data)
            else:
                g1 = f.create_group('/MDF/images/0')
                g1.attrs['EMAN.apix_x'] = np.array([1.0],dtype='f')
                g1.attrs['EMAN.apix_y'] = np.array([1.0],dtype='f')
                g1.attrs['EMAN.apix_z'] = np.array([1.0],dtype='f')
                g1.attrs['EMAN.nx'] = np.array([self.data.shape[0]])
                g1.attrs['EMAN.ny'] = np.array([self.data.shape[1]])
                g1.attrs['EMAN.nz'] = np.array([1])
                g1.create_dataset('image', data = self.data)
                g2 = f['/MDF/images']
                g2.attrs['imageid_max'] = np.array([0])

def rexcp(image_in, image_out):
    if image_in.endswith('.smv'):
        header_dict, data = get_smv_data(image_in)
    
    if image_out.endswith('.pkl'):
        with open(image_out, 'wb') as f:
            pickle.dump({'header_dict':header_dict, 'data':data}, f, protocol=pickle.HIGHEST_PROTOCOL)