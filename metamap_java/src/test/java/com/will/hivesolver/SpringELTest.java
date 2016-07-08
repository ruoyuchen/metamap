package com.will.hivesolver;

import com.will.StringUs;
import com.will.hivesolver.util.ETLUtils;
import junit.framework.TestCase;
import org.junit.Test;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.TypedValue;
import org.springframework.expression.common.TemplateParserContext;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;

/**
 * Created by will on 16-7-8.
 */
public class SpringELTest extends TestCase {
    @Test
    public void testFirst() throws Exception {
        ExpressionParser parser = new SpelExpressionParser();
        String randomPhrase = parser.parseExpression(
                "random number is #{T(java.lang.Math).random()}",
                new TemplateParserContext()).getValue(String.class);
        int two = parser.parseExpression("1 + 1").getValue(Integer.class); // 2
        assertEquals(two, 2);

        String testString = parser.parseExpression(
                "'test' + ' ' + 'string'").getValue(String.class); // test string
        assertEquals(testString, "test string");
// Subtraction
        int four = parser.parseExpression("1 - -3").getValue(Integer.class); // 4
        assertEquals(4, four);

// Operator precedence
        int minusTwentyOne = parser.parseExpression("1+2-3*8").getValue(Integer.class); // -21
        assertEquals(minusTwentyOne, -21);

        System.out.println(randomPhrase);
    }

    @Test
    public void testT() throws Exception {
        ExpressionParser parser = new SpelExpressionParser();
        String randomPhrase = parser.parseExpression(
                "random number is #{T(java.lang.Math).random()}",
                new TemplateParserContext()).getValue(String.class);
        System.out.println(randomPhrase);
    }

    @Test
    public void testFunction() throws NoSuchMethodException {
        ExpressionParser parser = new SpelExpressionParser();
        StandardEvaluationContext context = new StandardEvaluationContext();

        context.registerFunction("reverseString",
                StringUs.class.getDeclaredMethod("reverseString", new Class[] { String.class }));

        String helloWorldReversed = parser.parseExpression(
                "#reverseString('hello')").getValue(context, String.class);
        System.out.println(helloWorldReversed);
    }

    /**
     *
     * @throws Exception
     */
    @Test
    public void testReallity() throws Exception {
        ExpressionParser parser = new SpelExpressionParser();
        StandardEvaluationContext context = new StandardEvaluationContext(new StringUs() {
        });
        context.registerFunction("reverseString",
                StringUs.class.getDeclaredMethod("reverseString", new Class[] { String.class }));

//        String reverseString = parser.parseExpression(
//                "random number is #{reverseString('hello')}").getValue(context, String.class);


        TypedValue rootObject = context.getRootObject();

        String reverseString = parser.parseExpression(
                "random number is #{reverseString('hello')}",
                new TemplateParserContext()).getValue(context, String.class);

//        String reverseString = parser.parseExpression(
//                "#reverseString(\"hello\")").getValue(context, String.class);

        String randomPhrase = parser.parseExpression(
                "random number is '#{T(com.will.hivesolver.util.DateUtil).getTodayDateTime()}'",
                new TemplateParserContext()).getValue(String.class);
        System.out.println(reverseString);
        System.out.println(randomPhrase);

        String getDateKeyStrFromNow = parser.parseExpression(
                "random number is '#{T(com.will.hivesolver.util.DateUtil).getDateKeyStrFromNow(-4)}'",
                new TemplateParserContext()).getValue(String.class);
        System.out.println(getDateKeyStrFromNow);

        String getDateKeyStr = parser.parseExpression(
                "random number is '#{T(com.will.hivesolver.util.DateUtil).getDateKeyStr('20150329',4)}'",
                new TemplateParserContext()).getValue(String.class);
        System.out.println(getDateKeyStr);
    }


    /**
     *
     * @throws Exception
     */
    @Test
    public void testReallity2() throws Exception {
        ExpressionParser parser = new SpelExpressionParser();
        StandardEvaluationContext context = new StandardEvaluationContext(new ETLUtils());

        context.registerFunction("getDateKeyStr",
                ETLUtils.class.getDeclaredMethod("getDateKeyStr", new Class[] { String.class, Integer.class }));
        String getDateKeyStr = parser.parseExpression(
                "random number is '#{getDateKeyStr('20150329',4)}'",
                new TemplateParserContext()).getValue(context, String.class);
        System.out.println(getDateKeyStr);
    }
}
