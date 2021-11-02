package fr.uga.yumi; //group the related classes in a package
import javax.ws.rs.core.Response; // Import the HTTP Response class

import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

//import com.sun.org.apache.xml.internal.serialize.IndentPrinter;


public class myAppUsingRWS {
	

	public static String readMod(String path){
		String payLoad = "";
    	try {
			File fileObj = new File(path);
			Scanner myReader = new Scanner(fileObj);
			String tempString="";
			while (myReader.hasNextLine()) {
				tempString = myReader.nextLine();
				if (! tempString.isEmpty()){
					payLoad = payLoad + tempString + "\n";
				}
			}
			myReader.close();
		} catch (FileNotFoundException e) {
			System.out.println(
					"An error occurred while reading the RAPID code,"
							+"\n please check the path.");
			e.printStackTrace();
		}
		return payLoad;
	}
	/*=================
	 *  --- Main ---  *
	 *================*/	
    public static void main(String[] args) {
       
        // Robot Part
    	RWS4Yumi cl = new RWS4Yumi("Default User","robotics");
        // RWS4Yumi cl = new RWS4Yumi("yumi","marvin2020");
		Response connectionStatus = cl.connect("yumi","Test_API","bbb","local");

    	// read RAPID code
    	// Left
     	String leftPath = "G:\\Grenoble\\Semester_4\\Project_Codes\\Problem_Domain\\New_Domain_Problem\\Rapid\\currLeft.mod";
     	//String leftPath = "G:\\Grenoble\\Semester_4\\Project_Codes\\Problem_Domain\\New_Domain_Problem\\Rapid\\caliber.mod";
     	String payLoadLeft =  readMod(leftPath);
     	cl.setModuleText("MainModule","T_ROB_L",payLoadLeft);
     	// Right
//     	String rightPath = "G:\\Grenoble\\Semester_4\\Project_Codes\\Problem_Domain\\New_Domain_Problem\\Rapid\\currRight.mod";
//     	String payLoadRight = readMod(rightPath);
//     	cl.setModuleText("MainModule","T_ROB_R",payLoadRight);

		 // RAPID Execution
		 cl.resetRAPIDProgramPointerToMain();
		 Response response = cl.startRAPIDExecution("continue","continue","once",
		 	"none","disabled","true");

		// Release mastership
		Response release = cl.mastershipRelease();
		// Response holdRMMP = cl.cancelHeldOrRequestedRMMP();
    }

}
