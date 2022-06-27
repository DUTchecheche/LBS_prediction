# Supplementary Material for "Prediction of Ligand Binding Sites Using Improved Blind Docking Method with a Machine Learning-Based Scoring Function"

How to use our method

(1)	Prepare the receptor and the ligand for LBS prediction. You can prepare the receptor and the ligand with AutodockTools (Morris et al., 2009) and OpenBabel (O'Boyle et al., 2011) or the recommended method for Autodock Vina 1.2.0 (see https://autodock-vina.readthedocs.io/en/latest/docking_basic.html).

(2)	Calculate the blind docking box. You can use AutodockTools to set up the docking box visually or use the script "blinddocking_box.py" to calculate the blind docking box automatically. The docking box should be a little larger than the entire protein. Note that the docking box size is set by the number of grid points in AutodockTools while the docking box size required for Vina is the actual size (Å). In the script, the size of the blind docking box is set to 1.05 times the length, width, and height of the protein. 

$ cd .\scripts

$ python blinddocking_box.py

 Please enter the path containing all the receptor files in format '.pdbqt':
 
 .\LBS_prediction_1pph\receptor
 
 Please enter the path where the config files will be saved:
 
 .\ LBS_prediction_1pph\config
 
(3)	Blind docking. Autodock Vina 1.1.2 (Trott and Olson, 2010), Autodock Vina 1.2.0 (Eberhardt et al., 2021), QuickVina-w (Hassan et al., 2017), and any other docking software based on Vina's scoring function can be used to perform blind docking. The docking parameters, "exhaustiveness", "num_modes", and "energy_range" can be set to 16, 9 ,5(kcal/mol) respectively. Five times blind docking for each pair of receptor and ligand is encouraged.

If Autodock Vina 1.2.0 is selected to perform blind docking, you can use the following command to get the affinity descriptor:

$ cd .\LBS_prediction_1pph

$ Vina1.2.0 --config .\config\config.txt --receptor .\receptor\trypsin.pdbqt --ligand .\ligand\NAPAP.pdbqt --out .\docking_results\blinddocking1\trypsin-NAPAP-1.pdbqt --verbosity 2

If other docking software based on the old version of Vina is selected, the detailed score for affinity can be gained from the docking conformations with the docking parameter "—score_only". An example is as follows:

$ cd .\LBS_prediction_1pph

$ QuickVina-w --config .\config\config.txt --receptor .\receptor\trypsin.pdbqt --ligand .\ligand\NAPAP.pdbqt --out .\docking_results\blinddocking1\trypsin-NAPAP-1.pdbqt 

$ Vina_split --input .\docking_results\blinddocking1\trypsin-NAPAP-1.pdbqt --ligand .\docking_results\blinddocking1\trypsin-NAPAP-1-

$ QuickVina-w --receptor .\receptor\trypsin.pdbqt --ligand . \docking_results\blinddocking1\trypsin-NAPAP-1-1.pdbqt --score_only

(4)	Calculate the amino acid composition preference descriptor. The Python script "calculate_preference.py" can be used to calculate the descriptor quickly. Note that the docking conformations should be split before running "calculate_preference.py".

$ cd .\scripts

$ python calculate_preference.py

 Please enter the receptor file(.pdbqt):
 
 ..\LBS_prediction_1pph\receptor\trypsin.pdbqt
 
 Please enter the path where all the docking conformations are saved:
 
 ..\LBS_prediction_1pph\docking_results\blinddocking1
 
 Please enter the path where the result will be saved(aminoacid_preference.csv):
 
..\ LBS_prediction_1pph

(5)	Calculate the pocket characteristic descriptor. The pocket characteristic descriptor is calculated using Fpocket3.0 (Le Guilloux et al., 2009). Fpocket3.0 doesn't offer support for Windows. For more information about how to use it, please see http://fpocket.sourceforge.net/manual_fpocket2.pdf. First, you need to combine each docking conformation with its receptor as a complex file, and then use the dpocket module in Fpocket3.0 to calculate the pocket characteristic descriptor. You can use the following command in Linux:

$ dpocket -f complex.txt -v 10000

"complex.txt" contains the name and the path of all the complexes.

(6)	Prepare the input file of the ANN model. The three sets of descriptors obtained from the above steps should be summarized in a ".csv" table in the same format as the example "input_descriptors_from_BD.csv" (contents of the column "label" can be omitted). Take care not to change the order and position of the descriptors. 

(7)	Perform LBS prediction. Now you can run the script "load_model&prediction.py" to perform LBS prediction. The prediction results,  "output_LBSprediction_results.csv", can be found in the same level folder as the script. A Python3 environment with the Python packages: PyTorch, numpy, and pandas is required.

$ python load_model&prediction.py

 Please enter the path and name of the input file (.csv):
 
 .\LBS_prediction_1pph\input_descriptors_from_BD.csv

