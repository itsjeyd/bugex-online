package de.unisl.cs.st;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.util.CheckClassAdapter;

public class FactExtractingClassLoader extends ClassLoader {

	protected class CodeLocationsExtractingVisitor extends ClassVisitor {

		private String className;
		private String currentMethod;
		int firstLine = -1;
		int lastLine = -1;

		public CodeLocationsExtractingVisitor(String className, ClassWriter cw) {
			super(Opcodes.ASM4, cw);
			this.className = className;
		}

		@Override
		public void visitEnd() {
			addFact();
		}

		@Override
		public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
			MethodVisitor superMV = super.visitMethod(access, name, desc, signature, exceptions);
			if (name.equals("<init>") || name.equals("<cinit>") || className.equals(testClass)) {
				return superMV;
			}
			if (currentMethod != null) {
				addFact();
			}
			currentMethod = name;
			return new MethodVisitor(Opcodes.ASM4, superMV) {
				@Override
				public void visitLineNumber(int line, Label start) {
					if (firstLine == -1) {
						firstLine = line;
					} else {
						lastLine = line;
					}
					super.visitLineNumber(line, start);
				}
			};
		}

		private void addFact() {
			if (firstLine == -1) {
				return;
			}
			Fact fact = new Fact();
			fact.setClassName(className);
			fact.setMethodName(currentMethod);
			fact.setLineNumber(BugExMock.getRandomNumber(firstLine, lastLine));
			fact.setExplanation(generateExplanation());
			fact.setFactType(BugExMock.getRandomFactType());
			facts.add(fact);
		}

		private String generateExplanation() {
			//return "this is just shitty code...";
			return BugExMock.getRandomExplanation();
		}
	}

	private final org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(FactExtractingClassLoader.class);

	final List<Fact> facts = new ArrayList<Fact>();
	final String testClass;

	public FactExtractingClassLoader(String testCaseClass) {
		this.testClass = testCaseClass;
	}

	public List<Fact> getFacts() {
		return facts;
	}

	@Override
	public Class<?> loadClass(String fullyQualifiedTargetClass) throws ClassNotFoundException {
		if (isSystemClass(fullyQualifiedTargetClass)) {
			logger.info("Not instrumenting class '{}'.", fullyQualifiedTargetClass);
			return super.loadClass(fullyQualifiedTargetClass);
		}
		logger.info("Instrumenting class '{}'.", fullyQualifiedTargetClass);
		String className = fullyQualifiedTargetClass.replace('.', '/');
		InputStream is = java.lang.ClassLoader.getSystemResourceAsStream(className + ".class");
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

	protected boolean isSystemClass(String className) {
		if (className.startsWith("java.")) {
			return true;
		}
		if (className.startsWith("sun.")) {
			return true;
		}
		if (className.startsWith("org.junit.") || className.startsWith("junit.framework")) {
			return true;
		}
		return false;
	}

}
