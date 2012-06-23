package de.unisl.cs.st;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

import com.thoughtworks.xstream.XStream;

import de.unisl.cs.st.Fact.FactType;

public class BugExMock {

	private static final org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(BugExMock.class);

	public static FactType getRandomFactType() {
		FactType[] values = FactType.values();
		return values[getRandomNumber(0, values.length - 1)];
	}

	public static int getRandomNumber(int min, int max) {
		return min + (int) (Math.random() * ((max - min) + 1));
	}

	/**
	 * 1st argument: path of jar archive with failing test case
	 * 2nd argument: failing test case
	 * 3rd argument (optional): path of output file
	 * 4th argument (optional): artificial delay in seconds (for testing/simulating  purpose)
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length < 2) {
			System.out.println("Specify archive and failing test case that BugEx should analyse.");
			System.exit(-1);
			return;
		}

		// check input archive
		if (args[0] != null) {
			// input archive path is specified
			if (!isSupported(args[0])) {
				System.out.println("Input archive path is not valid: '"+args[0]+"' (Archive not supported!)");
				System.exit(-1);
				return;
			}
		}
		
		// check output path
		String outputPath = "";
			
		if (args.length > 2 && args[2] != null) {
			// output path is specified
			if (!args[2].endsWith("/")) {
				System.out.println("Output path is not valid: '"+args[2]+"' (No trailing '/')");
				System.exit(-1);
				return;
			} else {
				outputPath = args[2];
			}
		}
		
		// check for artificial delay
		long delayInMillis = 0l;
		
		if (args.length > 3 && args[3] != null) {
			long delayInSeconds = Long.parseLong(args[3]);
			if (delayInSeconds > 0)
				delayInMillis = delayInSeconds*1000;
		}

		List<Fact> facts = new BugExMock(args[0],args[1]).explainFailure();
		
		if (delayInMillis > 0) {
			System.out.println("Delaying process for "+delayInMillis/1000+" seconds..");
			
			try {
				Thread.sleep(delayInMillis);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
			System.out.println("Waking up..");
		}
		
		exportToXml(facts, outputPath);
		System.exit(0);
	}
	
	/**
	 * First argument: failing test case
	 * Third argument (optional): path of output file
	 * @param args
	 */
	public static void mainOld(String failingTest, String outputPath) {
		if (failingTest == null || failingTest.isEmpty()) {
			System.out.println("Specify failing test case that BugEx should analyse.");
			return;
		}
		
		// check output path
		if (outputPath != null) {
			// output path is specified
			if (!outputPath.endsWith("/")) {
				System.out.println("Output path is not valid: '"+outputPath+"' (No trailing '/')");
				return;
			}
		}

		List<Fact> facts = new BugExMock(failingTest).explainFailure();
		
		exportToXml(facts, outputPath);
	}

	private static void exportToXml(List<Fact> facts, String outputPath) {
		String oPath = outputPath == null ? "" : outputPath;		
		XStream xstream = new XStream();
		xstream.alias("fact", Fact.class);
		BufferedWriter writer = null;
		try {
			File file = new File(oPath+"bugex-results.xml");
			logger.info("Exporting {} facts to '{}'.", facts.size(), file.getCanonicalPath());
			writer = new BufferedWriter(new FileWriter(file));
			writer.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
			writer.newLine();
			writer.write("<facts>");
			writer.newLine();
			for (Fact fact : facts) {
				String xml = xstream.toXML(fact);
				writer.write(xml);
				writer.newLine();
			}
			writer.write("</facts>");
		} catch (Exception exc) {
			exc.printStackTrace();
		} finally {
			if (writer != null) {
				try {
					writer.close();
				} catch (IOException exc) {
					// muted
				}
			}
		}
	}

	private final Class<?> failingTestCase;
	private final FactExtractingClassLoader factExtractingClassLoader;

	public BugExMock(String qualifiedFailingTestCase) {
		logger.info("BugEx rocks.");
		logger.info("Analysing test '{}'.", qualifiedFailingTestCase);
		if (!qualifiedFailingTestCase.contains("#")) {
			throw new RuntimeException("Need to specify test method!");
		}
		String testCaseClass = qualifiedFailingTestCase.split("#")[0];
		factExtractingClassLoader = new FactExtractingClassLoader(testCaseClass);
		try {
			failingTestCase = factExtractingClassLoader.loadClass(testCaseClass);
		} catch (ClassNotFoundException exc) {
			throw new RuntimeException(exc);
		}
	}
	
	public BugExMock(String inputArchivePath, String qualifiedFailingTestCase) {
		logger.info("BugEx rocks #2.");
		logger.info("Analysing input archive '{}'.", inputArchivePath);
		if (!isSupported(inputArchivePath)) {
			throw new RuntimeException("Need to specify valid input archive!");
		}
		logger.info("Analysing test '{}'.", qualifiedFailingTestCase);
		if (!qualifiedFailingTestCase.contains("#")) {
			throw new RuntimeException("Need to specify test method!");
		}
		String testCaseClass = qualifiedFailingTestCase.split("#")[0];
		factExtractingClassLoader = new FactExtractingExternalClassLoader(inputArchivePath,testCaseClass);
		try {
			failingTestCase = factExtractingClassLoader.loadClass(testCaseClass);
		} catch (ClassNotFoundException exc) {
			throw new RuntimeException(exc);
		}
	}

	public List<Fact> explainFailure() {
		runTest();
		List<Fact> facts = factExtractingClassLoader.getFacts();
		if (facts.isEmpty()) {
			throw new RuntimeException("Something went wrong analysing the class file: Got no code locations! "
					+ "Was the code compiled with the -g option?");
		}
		return facts.subList(0, getRandomNumber(1, facts.size()));
	}

	private void runTest() {
		// TODO Make JUnit run only the specified test method
		Result result = JUnitCore.runClasses(failingTestCase);
		if (result.getFailures().isEmpty()) {
			throw new RuntimeException("Need a failing test to explain!");
		}
		Failure failure = result.getFailures().iterator().next();
		logger.info("Analyzing failure '{}' in '{}'.", failure.getException(), failure.getDescription());
	}
	
	/**
	 * currently jar and zip are supported
	 * 
	 * @param inputArchivePath
	 * @return
	 */
	static private boolean isSupported(String inputArchivePath) {
		if (inputArchivePath.endsWith(".jar") || inputArchivePath.endsWith(".zip"))
			return true;
		
		return false;
	}

}
