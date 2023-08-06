# This file is part of the GwDataManager package.
# Import data from various location into a dictionary-like object.
# 

"""
GwDataManager
=============

This module defines the following class(es)

--------------- --------------------------------------------
`Dataset`       Basically, it is an enhanced version of
                h5py Dataset class. This is the basic object
`GwDataManager` Basic class to read and manipulate GW data
`GlitchDB`      To be decided if mantained or not
--------------- --------------------------------------------

This is based on `h5py` classe File and Datase, with some modifications.
In particular, the class Dataset comprizes some new methods and properties
to make it more easy to manipulate.
"""

import sys, time
import numpy as np
from os.path import join, isfile
from glob import glob
from multiprocessing import Pool, cpu_count

# For the base classes and their extentions
import h5py
# For File object stored in memory or as temprary file
from io import BytesIO
from tempfile import TemporaryFile
# To define wrappers to enhance existing classes
from functools import wraps

# For the class FindGlitches (to be discontinued?)
from pandas import DataFrame, read_hdf

# Locations of ffl
from . import ffl_paths

# imports related to gwdama
from .gwLogger import GWLogger

# Necessary to fetch open data and to handle gps times
from gwpy.timeseries import TimeSeries, TimeSeriesDict
from gwpy.time import to_gps


# ----- Utility functions -----

def _add_property(cls):
    """
    Decorator to add properties to already existing classes.
    Partially based on the work of M. Garod:
    https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    
    Example
    -------
    To add theproperty `func` to the class Class:
    @_add_property(Class)
    def func(self):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, property(wrapper))
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator


def _add_method(cls):
    """
    Decorator to add methds to already existing classes.
    Partially based on the work of M. Garod:
    https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    
    Example
    -------
    To add theproperty `func` to the class Class:
    @_add_method(Class)
    def func(self):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator


@_add_property(h5py.Dataset)
def data(self):
    """
    Returns the content of an h5py Dataset in an easy looking way.
    Analogue of: dset[...]
    """
    return self[...]

@_add_property(h5py.Dataset)
def show_attrs(self):
    """
    Method that make a Dataset to 'show the attributes'
    """
    to_print = ''
    for k, val in self.attrs.items():
        to_print += "{:>10} : {}\n".format(k, val)
    #return to_print
    print(to_print)
              
def recursive_struct(group, indent = '  '):
    """
    Function to print a nice tree structure:
    │
    ├──
    └──
    """
    to_print = ''
    if isinstance(group, h5py.Group):
        for i,k in enumerate(group.keys()):
            if i+1<len(group.keys()):
                to_print += indent + f"├── {k}\n"
            else:
                to_print += indent + f"└── {k}\n"
                
            if isinstance(group[k], h5py.Group) and (i+1<len(group.keys())):
                to_print += recursive_struct(group[k], indent=indent+'│   ')
            elif isinstance(group[k], h5py.Group):
                to_print += recursive_struct(group[k], indent=indent+'    ')
                  
    return to_print 
    
def kay_changer(obj, key=None):
    """
    Check if a key is present in a dictionary-like object.
    If already present, change its name adding '_#', with increasing
    numbers.
    """
    if key is None:
        key = 'key'  # Default value
    if key in obj.keys():
        expand = 0
        while True:
            expand += 1
            new_key = key +'_'+ str(expand)
            if new_key in obj.keys():
                continue
            else:
                key = new_key
                break
    return key
    
def find_run(gps_start, gps_stop, host='https://www.gw-openscience.org'):
    """
    Given gps_start and gps_stop, it returns the run the data belongs to,
    otherwise it rises an error: data not belonging to gwosc
    """
    from gwosc.datasets import find_datasets
    from gwosc.datasets import event_gps, run_segment 
    all_runs = find_datasets(type='run',segment=(gps_start,gps_stop),)
    
    # Remove this not to mess up with things
    try:
        all_runs.remove('BKGW170608_16KHZ_R1')
    except:
        pass
    
    run = all_runs[0]
    for r in all_runs:
        if r[:2] in run:
            pass
        else:
            raise Exception('Too many data to recover! Check gps times!') 
    return run[:2]
    
# def name_changer(obj, kay):
#     if not os.path.exists(outdir):
#         os.makedirs(outdir)
#     else:
#         expand = 0
#         while True:
#             expand += 1
#             new_event = event_id +'_'+ str(expand)
#             if os.path.exists(args.directory.rstrip('/')+'/'+new_event):
#                 continue
#             else:
#                 event_id = new_event
#                 break
#         outdir = args.directory.rstrip('/')+'/'+event_id
#         os.makedirs(outdir)	

# ----- The Class -----

class GwDataManager(h5py.File):
    """
    New GwDataManager implementation.
    
    The standard behaviour is that the GwDataManager object (h5py.File) is
    initialized as a TemporaryFile(). Than it is filled with Datasets, and then
    saved on disk.
    If the provided `dama_name` mathces with the path/name.h5 of an existing file
    then there are options to import its content as a TempFile(), as before,
    or modified by means of this GwDataManager. In the latter case, it is recommended
    to close the file after palying with it.
    
    Parameters
    ----------
    dama_name : str
        Name of the `GwDataManager` object
    mode : str, optional
        r:  Read only, file must exist
        r+: Read/write, file must exist
        w:  Create file, truncate if exists (default)
        w- or x: Create file, fail if exists
        a:  Read/write if exists, create otherwise (default)
    storage : str, optional
        Only for mode in ('w','w-','x'). It determines where to store
        the content of this dataset while using it:
        'mem' for random access memory (default),
        'tem' for temporary file.
        The latter should be preferred for very large amounts of data.
        The former is expected to be faster.
        
    Examples
    --------
    Not available
        
    Notes
    -----
    Not available
        
    Raises
    ------
         
    """
    # NOTE: put methods in alphbetical order!
   
    def __init__(self, dama_name="mydama", mode='w', storage='mem', **kwargs):

        # Create a File object pointing to a TemporaryFile
        if mode in ('w','w-','x'):
            if storage  == 'mem':
                tf = BytesIO()
            elif storage == 'tmp':
                tf = TemporaryFile()
            else:
                raise ValueError("Unrecognised storage mode. Please, choose either 'mem' or 'tmp'")
            super().__init__(tf, mode=mode, **kwargs)
            
            # If name matches with something already existing, get its content
            try:
                with h5py.File(dama_name, 'r') as existing_dama:
                    for k in existing_dama.keys():
                        existing_dama.copy(k,self)
                    for k in existing_dama.attrs.keys():
                        self.attrs[k] = existing_dama.attrs[k]
                    print("Reading dama")

            except(OSError,):
                if mode == 'r+':
                    print('Creating new dama')
                self.attrs['dama_name'] = dama_name
                self.attrs['time_stamp']=str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))
        
        elif mode in ('r','a','r+'):
            try:
                super().__init__(dama_name, mode=mode,**kwargs)
                print("Reading dama")
            except(OSError,):
                print('Impossible to read dama. Creating a new one')
                if storage  == 'mem':
                    tf = BytesIO()
                elif storage == 'tmp':
                    tf = TemporaryFile()
                else:
                    raise ValueError("Unrecognised storage mode. Please, choose either 'mem' or 'tmp'")
                super().__init__(tf, mode=mode,**kwargs)
                self.attrs['dama_name'] = dama_name
                self.attrs['time_stamp']=str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))
                
        if "dama_name" not in self.attrs.keys():
            self.attrs['dama_name'] = "my_dama"
  
    def __repr__(self):
        """
        String representation of the object.
        """
        str_to_print = f"<{type(self).__name__} object at {hex(id(self))}: {self.attrs['dama_name']}>"
        #for k, val in self.__data_dict.items():
        #    str_to_print +="\n  {:>8} : {}".format(k,val.__repr__())
        return str_to_print
    
    def __str__(self):
        str_to_print = f"{self.attrs['dama_name']}:\n"+ recursive_struct(self)
 
        str_to_print += "\n  Attributes:\n"
        for k, val in self.attrs.items():
            str_to_print += "  {:>12} : {}\n".format(k, val)

        return str_to_print
    
    @property
    def show_attrs(self):
        """
        Method that make a Dataset to 'show the attributes'
        """
        to_print = ''
        for k, val in self.attrs.items():
            to_print += "{:>10} : {}\n".format(k, val)
        #return to_print
        print(to_print)
    
    def read_gwdata(self, m_tstart_gps, m_tstop_gps, m_data_source="gwosc-cvmfs", m_data_format="hdf5",
                    dts_key = 'key', m_channels=None, duplicate='rename', m_channel_name=None, **kwargs):
        """   
        Read data from different sources and append them to the main data manager.

        Parameters
        ----------
        m_tstart_gps : LIGOTimeGPS, float, str
            GPS start time of required data (TODO: defaults to start of data found); any input parseable by to_gps is fine
        m_tstop_gps : LIGOTimeGPS, float, str, optional
            GPS stop time of required data (TODO: defaults to start of data found); any input parseable by to_gps is fine
        m_data_source : str, optional
            defines the way data are read, and from where
        m_data_format : str, optional
            preferred data format to read
        dts_key : str, optional
            name of the dictionary to append to the GwDataManager
        m_channel_name : str, optional
            To be implemented     
        duplicate : str, optional
            If we try to append a dataset with an already existing key, we have the possibility
            to replace the previous one (deleting its content) or renaming the corresponding
            key by means of the `replace_key` function: "existing_key" -> "exisitng_key_1".
            Default "rename".
        **kwargs
            any other keyword arguments are passed to the `TimeSeries.read`
            method that parses the file that was downloaded

        Returns
        -------
        GwDataManager
        
        Examples
        --------
        Import data from online gwosc:
        
        >>> e_gps = to_gps("2017-08-14 12:00") # Gps time of GW170814
        >>> dama = GwDataManager()  # Default name 'mydama' assigned to the dictionary
        >>> dama.read_gwdata(e_gps - 50, e_gps +10, ifo='L1', m_data_source="gwosc-remote")
        
        Notes
        -----
        Not available
        
        Raises
        ------
        RuntimeError
            every time a wrong data source is provided
            
        """
        if (duplicate == "replace") and (dts_key in self.keys()):
            del self[dts_key]
        elif (duplicate == "rename") and (dts_key in self.keys()):
            dts_key = kay_changer(self, key=dts_key)
        elif (dts_key in self.keys()):
            raise Exception("Unrecognised 'duplicate' parameter. Please, select either 'rename' or 'replace'.") 
        else:
            pass
        
        dict_dataset = None

        if m_data_source == "gwosc-cvmfs":
            dataset = self.read_gwdata_gwosc_cvmfs(m_tstart_gps, m_tstop_gps,
                                                        m_data_format=m_data_format,
                                                        m_channels=m_channels,
                                                        **kwargs)
        elif m_data_source == "virgofarm":
            dataset = self.read_from_virgo(m_channels, m_tstart_gps, m_tstop_gps, **kwargs)       
            
        elif m_data_source == "gwosc-remote":
            dataset = self.read_gwdata_gwosc_remote(m_tstart_gps, m_tstop_gps,
                                                         data_format=m_data_format,
                                                         **kwargs)
        else:
            raise RuntimeError("Data source %s not yet implemented" % m_data_source)
    
        
        # Check wether the `dataset` is a gwpy TimeSeries or TimeSeriesDict:        
        if isinstance(dataset, TimeSeriesDict):
            grp = self.create_group(dts_key)
            for k in dataset.keys():
                dset = grp.create_dataset(k, data= dataset[k].data)
                dset.attrs.create('t0', dataset[k].t0)
                dset.attrs.create('unit', str(dataset[k].unit ))
                dset.attrs.create('channel', str(dataset[k].channel))
                dset.attrs.create('sample_rate', str(dataset[k].sample_rate.value))


        elif isinstance(dataset, TimeSeries):
            dset = self.create_dataset(dts_key, data= dataset.data)
            dset.attrs.create('t0', dataset.t0)
            dset.attrs.create('unit', str(dataset.unit ))
            dset.attrs.create('channel', str(dataset.channel))
            dset.attrs.create('sample_rate', str(dataset.sample_rate.value))
            if isinstance(m_channel_name, str):
                dset.attrs.create('name', m_channel_name)
                
#            dset.attrs['t0'] = dataset.t0
#             dset.attrs['unit'] = dataset.unit
#             dset.attrs['channel'] = dataset.channel.value
#             if isinstance(m_channel_name, str):
#                 dset.attrs['name'] = m_channel_name
        
        # finally, create the dataset with
#         ds = self.create_dataset(dts_key, data=dict_dataset.value)
        
#         ds.attrs['t0'] = dict_dataset.t0.value
#         ds.attrs['sample_rate'] = dict_dataset.sample_rate.value
#         if m_channels is not None:
#             ds.attrs['name'] = m_channel_name.value
#         if dict_dataset.unit is not None:
#             ds.attrs['unit'] = dict_dataset.unit.value
                     
    @staticmethod
    def _search_cvmfs(m_tstart_gps=None, m_tstop_gps=None,ifo='V1', rate='4k', m_data_format='hdf5',
                      cvmfs_path='/data2/cvmfs/gwosc.osgstorage.org/gwdata/'):
        """This methood searches the files corresponding to a given format in the
        provided gps time interval, science run (S5, S6, O1 or O2) and interferometer.

        In practice this is a twin of the ``find_gwf`` class method, meant to be
        used primarily on PC-Universe2, where cvmfs is mounted in the provided path,
        or on any other machine changing the path to cvmfs accordignly.

        Parameters
        ----------
        start : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            starting gps time where to find the frame files.
            Default: 1126259462.4 for O1, 1187008882.4 for O2,
            Error for any other choice of run.
            
        end : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            final gps time where to find the frame files. If ``start``
            is not provided, this is automatically set to 60 seconds.
            
        run : str, optional
            Name of the run where to read the data. Available options: 
                S5, S6, O1, or O2 (default)
        
        ifo : str, optional
            Name of the interferometer to read the data. Available options: 
                H1, L1, or V1 (default, only for the last part of O2)
        
        cvmfs_path : str, optional
            Directory where to look for the hdf5 files. Default choice is the
            directory on PC-Universe2. Don't change this value unless you have
            your own cvmfs on your local machine.
     
        Returns
        -------
        gwf_paths : list of str 
            List of paths to the gwf/hdf5 file(s) in the provided interval.
            
        Notes
        -----
        Still in development.
        """
                
        # 0) Initialise some values if not provided
        if (m_tstart_gps is None):
            m_tstart_gps = 1126259462.4 - 30 # GW150914 - 30 seconds
            m_tstop_gps = m_tstart_gps + 60          # Overwrite the previous 'end'
            print('Warning! No gps_start provided. GW150914 - 30 sec chosen instead.')
        else:
            m_tstart_gps = to_gps(m_tstart_gps)
            
        if m_tstop_gps is None:
            m_tstop_gps = m_tstart_gps+60
            print('Warning! No gps_end provided. Duration set to 60 seconds.')     
        else:
            m_tstop_gps = to_gps(m_tstop_gps)
       
        run = find_run(m_tstart_gps, m_tstop_gps)
        
        # Check format and rate
        if m_data_format not in ('hdf5', 'gwf'):
            raise ValueError("Error!! Invalid data format!! It must be either hdf5 or gwf")
        elif m_data_format=='hdf5':
            frmtdir='hdf'
        elif m_data_format=='gwf':
            frmtdir='frame'
        
        if rate not in ('4k', '16k'):
            raise ValueError("Error!! Invalid rate! It must be either 4k or 16k. Remember that you can resample it later.")
        
        # 1) Define the path where to search the files               
        hdf5_paths = glob(join(cvmfs_path,run,'strain.'+rate,frmtdir+'.v1/',ifo,'**/*.'+m_data_format))
        
        # 2) Make a dictionary with start gps time as key, and path, duration, and end as vlas.
        gwf_dict = {int(float(k.split('-')[-2])): {'path': k,
                                                   'len':  int(float(k.split('-')[-1].rstrip(m_data_format))),
                                                    'stop': int(float(k.split('-')[-2]) + float(k.rstrip(m_data_format).split('-')[-1]))
                                                   }
                    for k in hdf5_paths}

        # 3) 
        mindict = {k: v for k, v in gwf_dict.items() if k <= m_tstart_gps}
        try:
            minvalue = max(mindict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Provided gps_start is before the beginning of the ffl.")            
        maxdict = {k: v for k, v in gwf_dict.items() if k >= m_tstart_gps and m_tstop_gps <= v['stop']}
        try:
            maxvalue = min(maxdict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Select new gps time interval or try another frame.")            
            
        gwf_paths = [v['path'] for k, v in gwf_dict.items() if k >= minvalue and k <= maxvalue and v['path'].endswith("."+m_data_format)]

        return gwf_paths
    
    def read_gwdata_gwosc_cvmfs(self, m_tstart_gps=None, m_tstop_gps=None, ifo='V1',
                                m_channels=None, nproc=1, rate='4k', m_data_format='hdf5',
                                do_crop=True, cvmfs_path='/data2/cvmfs/gwosc.osgstorage.org/gwdata/'):
        """
        This method search GW data in the cvmfs aschive with the `_search_cvmfs` method,
        and returns a dataset (either TimeSeries or TimeSeriesDict).
        
        Parameters
        ----------
        run : str, optional
            Name of the run where to read the data. Available options: 
                S5, S6, O1, or O2 (default)
        
        ifo : str, optional
            Name of the interferometer to read the data. Available options: 
                H1, L1, or V1 (default, only for the last part of O2)
        
        cvmfs_path : str, optional
            Directory where to look for the hdf5 files. Default choice is the
            directory on PC-Universe2. Don't change this value unless you have
            your own cvmfs on your local machine.
        
        m_tstart_gps : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            starting gps time where to find the frame files. Default: 10 seconds ago
            
        mtstop_gps : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            ending gps time where to find the frame file. If `m_tstart_gps` is not provided, and the default
            value of 10 secods ago is used instead, `mtstop_gps` becomes equal to `m_tstart_gps`+5. If `m_tstart_gps` is
            provided but not `mtstop_gps`, the default duration is set to 5 seconds as well
                   
        nproc : int, optional
            Number of precesses to use for reading the data. This number should be smaller than
            the number of threads that the machine is hable to handle. Also, remember to
            set it to 1 if you are calling this method inside some multiprocessing function
            (otherwise you will spawn an 'army of zombie'. Google it). The best performances
            are obtained when the number of precesses equals the number of gwf files from to read from.
            
        do_crop : bool, optional
            For some purpose, it can be useful to get the whole content of the gwf files
            corresponding to the data of interest. In this case, set this parameter as False.
            Otherwise, if you prefer the data cropped accordingly to the provided gps interval
            leave it True.
            
        Returns
        -------
        outGwDM : GwDataManager
            GwDataManager filled with the Datasets corresponding to the specifications
            provided in the input parameters.
        """    
        # -- Improvement ---------------------
        # It is a waste of lines of code to repeat the gps checks etc. in each  method.
        # This will be improved in a next release 
        
        
       # 0) Initialise some values if not provided
        if (m_tstart_gps is None):
            m_tstart_gps = 1126259462.4 - 30 # GW150914 - 30 seconds
            m_tstop_gps = m_tstart_gps + 60          # Overwrite the previous 'end'
            print('Warning! No gps_start provided. GW150914 - 30 sec chosen instead.')

        if m_tstop_gps is None:
            m_tstop_gps = m_tstart_gps+60
            print('Warning! No gps_end provided. Duration set to 60 seconds.')     
    
        run = find_run(to_gps(m_tstart_gps),to_gps(m_tstop_gps))
            
        # Check format and rate
        if m_data_format not in ('hdf5', 'gwf'):
            raise ValueError("Error!! Invalid data format!! It must be either hdf5 or gwf")
        if rate not in ('4k', '16k'):
            raise ValueError("Error!! Invalid rate! It must be either 4k or 16k. Remember that you can resample it later.")
        
        # If the name of the channel(s) has been provided, replace the 'ifo' with one matching
        if isinstance(m_channels,list):
            ifo = m_channels[0][:2]
        elif isinstance(m_channels,str):
            ifo = m_channels[:2]
        else:
            # Define the channel names
            if (m_data_format=='gwf') and (rate=='4k') and (run not in ('O2','O3a')):
                m_channels=[f'{ifo}:LOSC-STRAIN',f'{ifo}:LOSC-DQMASK' ,f'{ifo}:LOSC-INJMASK']  # 4k before O2
            elif (m_data_format=='gwf') and (rate=='4k'):
                m_channels=[f'{ifo}:GWOSC-4KHZ_R1_STRAIN',f'{ifo}:GWOSC-4KHZ_R1_DQMASK' ,f'{ifo}:GWOSC-4KHZ_R1_INJMASK'] # 4k since O2
            elif (m_data_format=='gwf') and (rate=='16k'):
                m_channels=[f'{ifo}:GWOSC-16KHZ_R1_STRAIN',f'{ifo}:GWOSC-16KHZ_R1_DQMASK' ,f'{ifo}:GWOSC-16KHZ_R1_INJMASK'] 
        
        # 1) Make a dictionary of hdf5 file paths corresponding to the provided specs

        # Find the paths to the gwf's
        pths = self._search_cvmfs(ifo=ifo, m_tstart_gps=m_tstart_gps, m_tstop_gps=m_tstop_gps,
                                  cvmfs_path=cvmfs_path, rate=rate, m_data_format=m_data_format)
        
        # If data are read from just one gwf/hdf5, crop it immediately
        if len(pths)==1 and do_crop:
            if m_data_format=='hdf5':
                out_dataset = TimeSeries.read(source=pths, start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps), nproc=nproc, format='hdf5.losc')
            elif m_data_format=='gwf':
                out_dataset = TimeSeriesDict.read(source=pths, channels=m_channels, start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps),
                                                  nproc=nproc, dtype=np.float64)               
        elif not do_crop:
            if m_data_format=='hdf5':
                out_dataset = TimeSeries.read(source=pths, nproc=nproc, format='hdf5.losc')
            elif m_data_format=='gwf':
                out_dataset = TimeSeriesDict.read(source=pths, channels=m_channels, nproc=nproc, dtype=np.float64)                
                           
        elif len(pths)>1:
            if m_data_format=='hdf5':
                try:
                    TS = TimeSeries.read(source=pths, nproc=nproc, format='hdf5.losc')
                    out_dataset = TS.crop(start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps))
                except ValueError:
                    print('WARNING!!! Selected data interval contains holes (missing data). Trying to fetch them form online gwosc' )
                    # Try to get it from online
                    try:
                        out_dataset = TimeSeries.fetch_open_data(ifo, start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps),
                                                                 tag=kwargs.get('tag','CLN'),format='hdf5', **kwargs)
                        out_dataset.sample_rate = sample_rate
                    except:
                        print('No way of obtaining this data... Sorry!' )
                        out_dataset = TimeSeries([])
                        pass
                
            elif m_data_format=='gwf':
                try:
                    out_dataset = TimeSeriesDict.read(source=pths, channels=m_channels, nproc=nproc, dtype=np.float64)
                    out_dataset = out_dataset.crop(start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps))
                except ValueError:
                    print('WARNING!!! Selected data interval contains holes (missing data). Trying to fetch them form online gwosc' )
                    # Try to get it from online
                    try:
                        out_dataset = TimeSeries.fetch_open_data(ifo, start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps),
                                                                 tag=kwargs.get('tag','CLN'),format='hdf5', **kwargs)
                        out_dataset.sample_rate = sample_rate
                    except:
                        print('No way of obtaining this data... Sorry!' )
                        out_dataset = TimeSeries([])
                        pass           

        else:
            # Return whole frame files: k*100 seconds of data
            if m_data_format=='hdf5':
                out_dataset = TimeSeries.read(source=pths, start=to_gps(m_tstart_gps), format='hdf5.losc')
            elif m_data_format=='gwf':            
                out_dataset = TimeSeriesDict.read(source=pths, channels=m_channels, nproc=nproc, dtype=np.float64)            
              
        return out_dataset
    
    @staticmethod
    def read_gwdata_gwosc_remote(tstart_gps, tstop_gps, ifo='V1', data_format="hdf5", rate='4k', **kwargs):
        """
        Read GWOSC data from remote host server, which is by default:
         host='https://www.gw-openscience.org'
        This method is based on GWpy `fetch_open_data`
        
        Parameters
        ----------
        ifo : str
            Either 'L1', 'H1' or 'V1', the two-character prefix of the IFO in which you are interested
        tstart_gps : 
            Start
        tstop_gps : 
            Stop
        name : str
            Name to give to this dataset
        data_format : hdf5 or gwf
            Data format
        **kwargs
            Any other keyword arguments are passed to the TimeSeries.fetch_open_data method og GWpy 
            
        Returns
        -------
        gwpy.timeseries.TimeSeries
        
        """
        if rate in ('4k', 4096):
            sample_rate = 4096
        elif rate in ('16k', 16384):
            sample_rate = 16384
        else:
            raise ValueError("Inconsistent 'rate' parameter for gwosc!!! It must be either '4k' or '16k'.")
        
        TS = TimeSeries.fetch_open_data(ifo, tstart_gps, tstop_gps, tag=kwargs.get('tag','CLN'),format=data_format,
                                        sample_rate=sample_rate, **kwargs)     
        TS.sample_rate = sample_rate
        return TS       

    def write_gwdama_dataset(self, m_output_filename=None, m_compression="gzip"):
        """
        Method to write the dataset into an hdf5 file.
        
        Parameters
        ----------
        m_output_filename : str, optional
            Name of the output file. Default: 'output_gwdama_{}.h5'.format(self.__time_stamp)
        m_compression : str, optional
            Compression level

        """

        # defaut name
        m_ds = {}
        if m_output_filename is None:
            m_output_filename = 'output_gwdama_{}.h5'.format(self.attrs['time_stamp'])

        if isfile(m_output_filename):
            print('WARNING!! File already exists.')
        m_creation_time = str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))

        with h5py.File(m_output_filename, 'w') as m_out_hf:
            m_out_hf.attrs["time_stamp"] = m_creation_time
            for a, val in self.attrs.items():
                if a != "time_stamp":
                    m_out_hf.attrs[a] = val
            for ki in self.keys():
                self.copy(ki,m_out_hf)

    @staticmethod
    def find_gwf(m_tstart_gps=None, m_tstop_gps=None, ffl_spec="V1raw", ffl_path=None):
        """Fetch and return a list of GWF file paths corresponding to the provided gps time interval.
        Loading all the gwf paths of the data stored at Virgo is quite time consuming. This should be
        done only the first time though. Anyway, it is impossible to be sure that all the paths
        are already present in the class attribute gwf_paths wihout loading them again and checking if
        they are present. This last part should be improved in order to speed up the data acquisition. 
        
        Parameters
        ----------
        m_tstart_gps : LIGOTimeGPS, float, str, optional
            starting gps time where to find the frame files. Default: 10 seconds ago
            
        m_tstop_gps : LIGOTimeGPS, float, str, optional
            ending gps time where to find the frame file. If ``m_tstart_gps`` is not provided, and the default
            value of 10 secods ago is used instead, `end` becomes equal to `m_tstart_gps`+5. If ``m_tstart_gps`` is
            provided but not ``end``, the default duration is set to 5 seconds as well
            
        ffl_spec : str, optional
            Specs of the ffl file to read, already saved. Available specs: V1raw, V1trend, V1trend100, H1, L1,  
                             V1O3a, H1O3a, L1O3a
            Use 'V1raw' (defoult) for fast Virgo channels. 

        ffl_path : str, optional
            Alternative to  ``ffl_specs``: if the path to a local ffl file is available, the gwf corresponding to the specified
            gps interval are read from it and ``ffl_specs`` is ignored.
                            
            
        Returns
        -------
        gwf_paths : `list`
            List of paths to the gwf file in the provided interval.
            
        Notes
        -----
        Calling this method multiple times overwrite the previously stored ones.
        """

        # 0) Initialise some values if not provided
        if (m_tstart_gps is None):
            m_tstart_gps = to_gps('now')-10
            m_tstop_gps = m_tstart_gps + 5          # Overwrite the previous 'end'
            print('Warning! No gps_start provided. Changed to 10 seconds ago, and 5 seconds of duration.')
        else:
            m_tstart_gps = to_gps(m_tstart_gps)
            
        if m_tstop_gps is None:
            m_tstop_gps = m_tstart_gps+5
            print('Warning! No gps_end provided. Duration set to 5 seconds.')     
        else:
            m_tstop_gps = to_gps(m_tstop_gps)
        
        # Definition of the ffl file
        if ffl_path is not None:
            ffl = ffl_path
        else:            
            # Find where to fetch the data
            # Virgo
            if ffl_spec=="V1raw":
                ffl = ffl_paths.V1_raw
            elif ffl_spec=="V1trend":
                ffl = ffl_paths.V1_trend
            elif ffl_spec=="V1trend100":
                ffl = ffl_paths.V1_trend100
            # at UniPi
            elif ffl_spec=="Unipi_O3":
                ffl = ffl_paths.unipi_O3
            elif ffl_spec=="Unipi_arch":
                ffl = ffl_paths.unipi_arch

            # O3a
            elif ffl_spec=="V1O3a":
                ffl = ffl_paths.V1_O3a
            elif ffl_spec=="H1O3a":
                ffl = ffl_paths.H1_O3a
            elif ffl_spec=="L1O3a":
                ffl = ffl_paths.L1_O3a    

            # LIGO data from CIT
            # >>>> FIX: multiple frame <<<<
            elif ffl_spec=="H1":
                if to_gps(m_tstop_gps)<(to_gps('now')-3700):
                    ffl = ffl_paths.H1_older
                elif to_gps(m_tstart_gps)>(to_gps('now')-3600):
                    ffl = ffl_paths.H1_newer
                else:
                    # <------ Fix reading from eterogeneous frames ----->
                    print("Warning!!! Data not available online and not stored yet")
            elif ffl_spec=="L1":
                if to_gps(m_tstop_gps)<(to_gps('now')-3700):
                    ffl = ffl_paths.L1_older
                elif to_gps(m_tstart_gps)>(to_gps('now')-3600):
                    ffl = ffl_paths.L1_newer
                else:
                    # <------ Fix reading from eterogeneous frames ----->
                    print("Warning!!! Data not available online and not stored yet")        
        
            # Reprocessed O3a data
            # <- insert here when ready ->

            else:
                raise ValueError("ERROR!! Unrecognised ffl spec. Check docstring")            

        # 1) Get the ffl (gwf list) corresponding to the desired data frame
        with open(ffl, 'r') as f:
            content = f.readlines()
            # content is a list (with hundreds of thousands of elements) of strings
            # containing the path to the gwf, the gps_start, the duration, and other
            # floats, usually equals to zero.
        content = [x.split() for x in content]
        
        # Make a dictionary with start gps time as key, and path, duration, and end as vlas.
        gwf_dict = {round(float(k[1])): {'path': k[0],
                                         'len': int(float(k[2])),
                                         'stop': round(float(k[1]) + int(float(k[2])))}
                    for k in content}

        # 2)
        mindict = {k: v for k, v in gwf_dict.items() if k <= m_tstart_gps}
        try:
            minvalue = max(mindict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Provided gps_start is before the beginning of the ffl.")            
        maxdict = {k: v for k, v in gwf_dict.items() if k >= m_tstart_gps and m_tstop_gps <= v['stop']}
        try:
            maxvalue = min(maxdict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Select new gps time interval or try another frame.")            
            
        gwf_paths = [v['path'] for k, v in gwf_dict.items() if k >= minvalue and k <= maxvalue and v['path'].endswith(".gwf")]

        return gwf_paths
    
    @classmethod
    def read_from_virgo(cls,m_channels, m_tstart_gps=None, m_tstop_gps=None, nproc=1, do_crop=True, **kwargs):
        """This method reads GW data from GWFs, fetched with the ``ffind_gwf`` method,
        and returns a TimeSeriesDictionary object filled with data.
        
        Parameters
        ----------
        m_channels : list of strings
            List with the names of the Virgo channels whose data that should be read.
            Example: channels = ['V1:Hrec_hoft_16384Hz', 'V1:LSC_DARM']
        
        m_tstart_gps : LIGOTimeGPS, float, str, optional
            starting gps time where to find the frame files. Default: 10 seconds ago
            
        m_tstop_gps : LIGOTimeGPS, float, str, optional
            ending gps time where to find the frame file. If `start` is not provided, and the default
            value of 10 secods ago is used instead, `end` becomes equal to `start`+5. If `start` is
            provided but not `end`, the default duration is set to 5 seconds as well
                   
        nproc : int, optional
            Number of precesses to use for reading the data. This number should be smaller than
            the number of threads that the machine is hable to handle. Also, remember to
            set it to 1 if you are calling this method inside some multiprocessing function
            (otherwise you will spawn an 'army of zombie'. Google it). The best performances
            are obtained when the number of precesses equals the number of gwf files from to read from.
            
        do_crop : bool, optional
            For some purpose, it can be useful to get the whole content of the gwf files
            corresponding to the data of interest. In this case, set this parameter as False.
            Otherwise, if you prefer the data cropped accordingly to the provided gps interval
            leave it True.
            
        kwargs : are the arguments to pass to the ``find_gwf`` method. In particular:
        
        ffl_spec : str, optional
            Available specs: V1raw, V1trend, V1trend100, H1, L1,  
                             V1O3a, H1O3a, L1O3a
            
        Returns
        -------
        outGwDM : GwDataManager object
            filled with the TimeSeries corresponding to the specifications provided in the input
            parameters.
        """

        if isinstance(m_channels, str):
            m_channels = [m_channels]
        
        # Find the paths to the gwf's
        pths = cls.find_gwf(m_tstart_gps=m_tstart_gps, m_tstop_gps=m_tstop_gps, ffl_spec=kwargs.get("ffl_spec","V1raw"),
                            ffl_path=kwargs.get('ffl_path'))
        
        # If data are read from just one gwf, crop it immediately
        if len(pths)==1 and do_crop:
            outTSD = TimeSeriesDict.read(source=pths, channels=m_channels, start=m_tstart_gps, end=m_tstop_gps,
                            nproc=nproc, dtype=np.float64)
        elif not do_crop:
            outTSD = TimeSeriesDict.read(source=pths, channels=m_channels, nproc=nproc, dtype=np.float64)

        elif len(pths)>1:
            outTSD = TimeSeriesDict.read(source=pths, channels=m_channels, nproc=nproc, dtype=np.float64)
            outTSD = outTSD.crop(start=to_gps(m_tstart_gps), end=to_gps(m_tstop_gps))
        else:
            # Return whole frame files: k*100 seconds of data
            outTSD = TimeSeriesDict.read(source=pths, channels=m_channels, nproc=nproc, dtype=np.float64)

        return outTSD

