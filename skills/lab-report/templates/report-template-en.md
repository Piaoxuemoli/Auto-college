# Default English Lab Report Template

Use this template when the user does not provide a custom template. This template structure follows standard university lab report format.

## Template Structure

```markdown
# <Experiment Title>

**<Institution Name>**
**<College/School Name>**
**Standard Lab Report**

---

**Course Name:** <Course Name>

---

| Item | Content |
|------|---------|
| **Name** | <Student Name> |
| **Student ID** | <ID> |
| **Class** | <Class Name> |
| **Experiment Date** | <Date> |
| **Instructor** | <Instructor Name> |
| **Lab Name** | <Lab Name> |

---

## 1. Experiment Name

<Experiment Name>

## 2. Experiment Project Name

<Experiment Project Name>

## 3. Objective

<Extracted from procedure_summary.md>

## 4. Experiment Content

<Extracted from procedure_summary.md>

## 5. Equipment (Devices and Components)

| Equipment/Software | Model/Version | Quantity/Notes |
|--------------------|---------------|----------------|
| <Equipment 1>      | <Model 1>     | <Notes>        |

<Extracted from procedure_summary.md>

## 6. Procedure and Operations

### Step 1: <Step Name>

<Step description and operations>

```bash
<command>
```

### Step 2: <Step Name>

<Step description and operations>

```bash
<command>
```

<!-- Add more steps as needed -->

## 7. Results and Data Analysis

### Step 1 Results

[TO BE FILLED]

[SCREENSHOT: step1]

### Step 2 Results

[TO BE FILLED]

[SCREENSHOT: step2]

<!-- Add more step results as needed -->

### Data Summary

| Metric | Value |
|--------|-------|
| <Metric 1> | [TO BE FILLED] |
| <Metric 2> | [TO BE FILLED] |

## 8. Conclusion

[TO BE FILLED]

## 9. Summary and Reflections

[TO BE FILLED]

## 10. Suggestions for Improvement

[TO BE FILLED]

---

**Report Score:** ____________

**Instructor Signature:** ____________

**Date:** ____________
```

## Usage Notes

- `[TO BE FILLED]` placeholders are replaced by the report-writer agent during final fill-in with actual data and analysis.
- `[SCREENSHOT: stepN]` placeholders are replaced with inline screenshots.
- Personal info fields (name, student ID, class, etc.) are auto-filled from `experiment_info.json`.
- Institution name, college name, and course name are auto-filled from `experiment_info.json`.
- Objective, content, equipment, and procedure are filled from `procedure_summary.md`.
- This template follows standard university lab report format; if the user specifies a custom template, it takes precedence.
