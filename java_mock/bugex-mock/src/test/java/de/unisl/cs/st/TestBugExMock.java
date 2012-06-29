package de.unisl.cs.st;

import org.junit.Before;
import org.junit.Test;

public class TestBugExMock {

	String failingArchive;
	String failingMethod;
	String outputPath;
	
	@Before
	public void initPath() {
		failingArchive = "/home/freddy/failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar";
		failingMethod = "de.mypackage.TestMyClass#testGetMin";
		outputPath = "/home/freddy/";
	}
	/*
	 * New main input tests (with input archive)
	 */
	@Test
	public void testMain(){
		BugExMock.main(new String[]{failingArchive,failingMethod});
	}
	
//	@Test
//	public void testMainCustomPath(){
//		BugExMock.main(new String[]{failingArchive,failingMethod,"/home/freddy"});
//	}
//	
//	/*
//	 * Old main method tests (without input archive)
//	 */
//	
//	@Test
//	public void testMainOld(){
//		BugExMock.mainOld("de.mypackage.TestMyClass#testGetMin",null);
//	}
//	
//	@Test
//	public void testMainOldCustomPath(){
//		BugExMock.mainOld("de.mypackage.TestMyClass#testGetMin","/home/freddy/");
//	}
}
