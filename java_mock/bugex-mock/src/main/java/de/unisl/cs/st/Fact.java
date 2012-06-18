package de.unisl.cs.st;

public class Fact {

	public static enum FactType {
		TYPE_A, TYPE_B;
	}

	private String className;
	private String methodName;
	private Integer lineNumber;
	private String explanation;
	private FactType factType;

	public String getClassName() {
		return className;
	}

	public String getExplanation() {
		return explanation;
	}

	public FactType getFactType() {
		return factType;
	}

	public Integer getLineNumber() {
		return lineNumber;
	}

	public String getMethodName() {
		return methodName;
	}

	public void setClassName(String className) {
		this.className = className;
	}

	public void setExplanation(String explanation) {
		this.explanation = explanation;
	}

	public void setFactType(FactType factType) {
		this.factType = factType;
	}

	public void setLineNumber(Integer lineNumber) {
		this.lineNumber = lineNumber;
	}

	public void setMethodName(String methodName) {
		this.methodName = methodName;
	}
}
