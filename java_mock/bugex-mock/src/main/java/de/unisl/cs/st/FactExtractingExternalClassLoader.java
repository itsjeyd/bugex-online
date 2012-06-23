package de.unisl.cs.st;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.util.CheckClassAdapter;

/**
 * This class loader accesses an external .jar archive to load a given class.
 * 
 * @author Frederik Leonhardt <frederik.leonhardt@googlemail.com>
 * @date 18/06/2012
 */
public class FactExtractingExternalClassLoader extends FactExtractingClassLoader {

	private final org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(FactExtractingExternalClassLoader.class);

	final String inputArchivePath;

	public FactExtractingExternalClassLoader(String inputArchivePath, String testCaseClass) {
		super(testCaseClass);
		this.inputArchivePath = inputArchivePath;
	}

	@Override
	public Class<?> loadClass(String fullyQualifiedTargetClass) throws ClassNotFoundException {
		if (isSystemClass(fullyQualifiedTargetClass)) {
			return super.loadClass(fullyQualifiedTargetClass);
		}
		logger.info("Instrumenting class '{}'.", fullyQualifiedTargetClass);
		
		// now it gets funky
		File jarFile = new File(inputArchivePath);
		URL jarFileURL;

		try {
			jarFileURL = jarFile.toURI().toURL();
		} catch (MalformedURLException e) {
			throw new RuntimeException(e);
		}
				
		//System.out.println("jar file url: "+jarFileURL.toString());
		
		// use new url class loader to load from external jar
		URLClassLoader urlClassLoader = new URLClassLoader(new URL[]{jarFileURL});
		
		// testing..
//		Class<?> clazz = Class.forName(fullyQualifiedTargetClass, true, urlClassLoader);
//		System.out.println("instance: "+clazz.toString());;

		// build path string to get input stream later on
		String className = fullyQualifiedTargetClass.replace('.', '/');
		InputStream is = urlClassLoader.getResourceAsStream(className + ".class");
		if (is == null) {
			throw new ClassNotFoundException("Class '" + fullyQualifiedTargetClass + "' could not be found!");
		}
		ClassReader reader = null;
		try {
			reader = new ClassReader(is);
		} catch (IOException exc) {
			throw new ClassNotFoundException();
		}
		ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_MAXS);
		ClassVisitor cv = new CodeLocationsExtractingVisitor(fullyQualifiedTargetClass, writer);
		CheckClassAdapter checkClassAdapter = new CheckClassAdapter(cv);
		reader.accept(checkClassAdapter, ClassReader.SKIP_FRAMES);
		byte[] byteBuffer = writer.toByteArray();
		Class<?> result = defineClass(fullyQualifiedTargetClass, byteBuffer, 0, byteBuffer.length);
		return result;
	}

}
