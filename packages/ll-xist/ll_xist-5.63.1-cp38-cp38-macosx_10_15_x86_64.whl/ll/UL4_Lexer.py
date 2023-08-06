# Generated from src/ll/UL4_Lexer.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2J")
        buf.write("\u02c7\b\1\b\1\b\1\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5")
        buf.write("\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f")
        buf.write("\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4")
        buf.write("\22\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27")
        buf.write("\t\27\4\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34")
        buf.write("\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#")
        buf.write("\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+")
        buf.write("\4,\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62")
        buf.write("\4\63\t\63\4\64\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48")
        buf.write("\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4")
        buf.write("A\tA\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4")
        buf.write("J\tJ\4K\tK\4L\tL\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4")
        buf.write("S\tS\4T\tT\4U\tU\3\2\6\2\u00b0\n\2\r\2\16\2\u00b1\3\2")
        buf.write("\3\2\3\3\5\3\u00b7\n\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\5\6\5\u00c3\n\5\r\5\16\5\u00c4\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\7\6\7\u00cd\n\7\r\7\16\7\u00ce\3\b\6\b\u00d2\n")
        buf.write("\b\r\b\16\b\u00d3\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\f")
        buf.write("\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\25")
        buf.write("\3\25\3\25\3\25\3\26\6\26\u0127\n\26\r\26\16\26\u0128")
        buf.write("\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\32")
        buf.write("\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34")
        buf.write("\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3 ")
        buf.write("\3 \3 \3 \3 \3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3\"\3")
        buf.write("#\3#\3#\3#\3$\3$\3$\3$\3$\3$\3%\3%\3%\3%\3%\3%\3%\3%\3")
        buf.write("%\3%\3%\3%\3&\3&\3&\3&\3&\3&\3&\3&\3&\3&\3&\3&\3&\3\'")
        buf.write("\3\'\3(\3(\3)\3)\3*\3*\3+\3+\3,\3,\3-\3-\3-\3.\3.\3/\3")
        buf.write("/\3\60\3\60\3\61\3\61\3\61\3\62\3\62\3\63\3\63\3\64\3")
        buf.write("\64\3\64\3\65\3\65\3\65\3\66\3\66\3\66\3\67\3\67\38\3")
        buf.write("8\38\39\39\3:\3:\3;\3;\3<\3<\3=\3=\3>\3>\3?\3?\3@\3@\3")
        buf.write("A\3A\7A\u01ba\nA\fA\16A\u01bd\13A\3B\3B\3C\3C\3D\3D\3")
        buf.write("E\3E\3F\6F\u01c8\nF\rF\16F\u01c9\3F\3F\3F\6F\u01cf\nF")
        buf.write("\rF\16F\u01d0\3F\3F\3F\6F\u01d6\nF\rF\16F\u01d7\3F\3F")
        buf.write("\3F\6F\u01dd\nF\rF\16F\u01de\5F\u01e1\nF\3G\3G\5G\u01e5")
        buf.write("\nG\3G\6G\u01e8\nG\rG\16G\u01e9\3H\6H\u01ed\nH\rH\16H")
        buf.write("\u01ee\3H\3H\7H\u01f3\nH\fH\16H\u01f6\13H\3H\5H\u01f9")
        buf.write("\nH\3H\3H\6H\u01fd\nH\rH\16H\u01fe\3H\5H\u0202\nH\3H\6")
        buf.write("H\u0205\nH\rH\16H\u0206\3H\3H\5H\u020b\nH\3I\3I\3I\3I")
        buf.write("\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\5I\u021d\nI\5I\u021f")
        buf.write("\nI\3J\3J\3J\3J\3J\3J\3J\3J\3J\3J\3J\3J\3J\3J\3K\3K\3")
        buf.write("K\3K\3K\3K\3K\3K\3K\3K\3K\3K\3K\3K\5K\u023d\nK\3K\3K\3")
        buf.write("L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3")
        buf.write("L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3L\5L\u025e\nL\3M\3M\3M\3")
        buf.write("M\3N\3N\3N\7N\u0267\nN\fN\16N\u026a\13N\3N\3N\3N\3N\7")
        buf.write("N\u0270\nN\fN\16N\u0273\13N\3N\5N\u0276\nN\3O\3O\3O\3")
        buf.write("O\3O\7O\u027d\nO\fO\16O\u0280\13O\3O\3O\3O\3O\3O\3O\3")
        buf.write("O\3O\7O\u028a\nO\fO\16O\u028d\13O\3O\3O\3O\5O\u0292\n")
        buf.write("O\3P\3P\3P\5P\u0297\nP\3P\3P\6P\u029b\nP\rP\16P\u029c")
        buf.write("\3Q\3Q\3Q\5Q\u02a2\nQ\3Q\3Q\6Q\u02a6\nQ\rQ\16Q\u02a7\3")
        buf.write("R\3R\3R\3R\3R\5R\u02af\nR\3S\3S\3S\3S\3S\3T\3T\3T\3T\3")
        buf.write("T\3T\3T\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\7\u00c4\u00ce")
        buf.write("\u0128\u027e\u028b\2V\6\3\b\4\n\5\f\6\16\7\20\b\22\t\24")
        buf.write("\n\26\13\30\f\32\r\34\16\36\17 \20\"\21$\22&\23(\24*\25")
        buf.write(",\26.\27\60\30\62\31\64\32\66\338\34:\35<\36>\37@ B!D")
        buf.write("\"F#H$J%L&N\'P(R)T*V+X,Z-\\.^/`\60b\61d\62f\63h\64j\65")
        buf.write("l\66n\67p8r9t:v;x<z=|>~?\u0080@\u0082A\u0084B\u0086\2")
        buf.write("\u0088\2\u008a\2\u008c\2\u008eC\u0090\2\u0092D\u0094\2")
        buf.write("\u0096E\u0098F\u009aG\u009cH\u009eI\u00a0J\u00a2\2\u00a4")
        buf.write("\2\u00a6\2\u00a8\2\u00aa\2\u00ac\2\6\2\3\4\5\21\4\2\13")
        buf.write("\13\"\"\5\2\13\f\17\17\"\"\5\2C\\aac|\6\2\62;C\\aac|\5")
        buf.write("\2\62;CHch\4\2DDdd\4\2QQqq\4\2ZZzz\4\2GGgg\4\2--//\6\2")
        buf.write("\f\f\17\17$$^^\6\2\f\f\17\17))^^\4\2$$^^\4\2))^^\n\2$")
        buf.write("$))^^cdhhppttvv\2\u02e8\2\6\3\2\2\2\2\b\3\2\2\2\2\n\3")
        buf.write("\2\2\2\2\f\3\2\2\2\3\16\3\2\2\2\3\20\3\2\2\2\4\22\3\2")
        buf.write("\2\2\4\24\3\2\2\2\4\26\3\2\2\2\4\30\3\2\2\2\4\32\3\2\2")
        buf.write("\2\4\34\3\2\2\2\4\36\3\2\2\2\4 \3\2\2\2\4\"\3\2\2\2\4")
        buf.write("$\3\2\2\2\4&\3\2\2\2\4(\3\2\2\2\4*\3\2\2\2\4,\3\2\2\2")
        buf.write("\4.\3\2\2\2\5\60\3\2\2\2\5\62\3\2\2\2\5\64\3\2\2\2\5\66")
        buf.write("\3\2\2\2\58\3\2\2\2\5:\3\2\2\2\5<\3\2\2\2\5>\3\2\2\2\5")
        buf.write("@\3\2\2\2\5B\3\2\2\2\5D\3\2\2\2\5F\3\2\2\2\5H\3\2\2\2")
        buf.write("\5J\3\2\2\2\5L\3\2\2\2\5N\3\2\2\2\5P\3\2\2\2\5R\3\2\2")
        buf.write("\2\5T\3\2\2\2\5V\3\2\2\2\5X\3\2\2\2\5Z\3\2\2\2\5\\\3\2")
        buf.write("\2\2\5^\3\2\2\2\5`\3\2\2\2\5b\3\2\2\2\5d\3\2\2\2\5f\3")
        buf.write("\2\2\2\5h\3\2\2\2\5j\3\2\2\2\5l\3\2\2\2\5n\3\2\2\2\5p")
        buf.write("\3\2\2\2\5r\3\2\2\2\5t\3\2\2\2\5v\3\2\2\2\5x\3\2\2\2\5")
        buf.write("z\3\2\2\2\5|\3\2\2\2\5~\3\2\2\2\5\u0080\3\2\2\2\5\u0082")
        buf.write("\3\2\2\2\5\u0084\3\2\2\2\5\u008e\3\2\2\2\5\u0092\3\2\2")
        buf.write("\2\5\u0096\3\2\2\2\5\u0098\3\2\2\2\5\u009a\3\2\2\2\5\u009c")
        buf.write("\3\2\2\2\5\u009e\3\2\2\2\5\u00a0\3\2\2\2\6\u00af\3\2\2")
        buf.write("\2\b\u00b6\3\2\2\2\n\u00bc\3\2\2\2\f\u00c2\3\2\2\2\16")
        buf.write("\u00c6\3\2\2\2\20\u00cc\3\2\2\2\22\u00d1\3\2\2\2\24\u00d5")
        buf.write("\3\2\2\2\26\u00e0\3\2\2\2\30\u00e4\3\2\2\2\32\u00e9\3")
        buf.write("\2\2\2\34\u00ed\3\2\2\2\36\u00f1\3\2\2\2 \u00f5\3\2\2")
        buf.write("\2\"\u00fb\3\2\2\2$\u00fe\3\2\2\2&\u0103\3\2\2\2(\u0108")
        buf.write("\3\2\2\2*\u0114\3\2\2\2,\u0121\3\2\2\2.\u0126\3\2\2\2")
        buf.write("\60\u012a\3\2\2\2\62\u012d\3\2\2\2\64\u0131\3\2\2\2\66")
        buf.write("\u0134\3\2\2\28\u0137\3\2\2\2:\u013c\3\2\2\2<\u0140\3")
        buf.write("\2\2\2>\u0143\3\2\2\2@\u0147\3\2\2\2B\u014a\3\2\2\2D\u014f")
        buf.write("\3\2\2\2F\u0154\3\2\2\2H\u015a\3\2\2\2J\u015e\3\2\2\2")
        buf.write("L\u0164\3\2\2\2N\u0170\3\2\2\2P\u017d\3\2\2\2R\u017f\3")
        buf.write("\2\2\2T\u0181\3\2\2\2V\u0183\3\2\2\2X\u0185\3\2\2\2Z\u0187")
        buf.write("\3\2\2\2\\\u0189\3\2\2\2^\u018c\3\2\2\2`\u018e\3\2\2\2")
        buf.write("b\u0190\3\2\2\2d\u0192\3\2\2\2f\u0195\3\2\2\2h\u0197\3")
        buf.write("\2\2\2j\u0199\3\2\2\2l\u019c\3\2\2\2n\u019f\3\2\2\2p\u01a2")
        buf.write("\3\2\2\2r\u01a4\3\2\2\2t\u01a7\3\2\2\2v\u01a9\3\2\2\2")
        buf.write("x\u01ab\3\2\2\2z\u01ad\3\2\2\2|\u01af\3\2\2\2~\u01b1\3")
        buf.write("\2\2\2\u0080\u01b3\3\2\2\2\u0082\u01b5\3\2\2\2\u0084\u01b7")
        buf.write("\3\2\2\2\u0086\u01be\3\2\2\2\u0088\u01c0\3\2\2\2\u008a")
        buf.write("\u01c2\3\2\2\2\u008c\u01c4\3\2\2\2\u008e\u01e0\3\2\2\2")
        buf.write("\u0090\u01e2\3\2\2\2\u0092\u020a\3\2\2\2\u0094\u020c\3")
        buf.write("\2\2\2\u0096\u0220\3\2\2\2\u0098\u022e\3\2\2\2\u009a\u025d")
        buf.write("\3\2\2\2\u009c\u025f\3\2\2\2\u009e\u0275\3\2\2\2\u00a0")
        buf.write("\u0291\3\2\2\2\u00a2\u0296\3\2\2\2\u00a4\u02a1\3\2\2\2")
        buf.write("\u00a6\u02ae\3\2\2\2\u00a8\u02b0\3\2\2\2\u00aa\u02b5\3")
        buf.write("\2\2\2\u00ac\u02bc\3\2\2\2\u00ae\u00b0\t\2\2\2\u00af\u00ae")
        buf.write("\3\2\2\2\u00b0\u00b1\3\2\2\2\u00b1\u00af\3\2\2\2\u00b1")
        buf.write("\u00b2\3\2\2\2\u00b2\u00b3\3\2\2\2\u00b3\u00b4\b\2\2\2")
        buf.write("\u00b4\7\3\2\2\2\u00b5\u00b7\7\17\2\2\u00b6\u00b5\3\2")
        buf.write("\2\2\u00b6\u00b7\3\2\2\2\u00b7\u00b8\3\2\2\2\u00b8\u00b9")
        buf.write("\7\f\2\2\u00b9\u00ba\3\2\2\2\u00ba\u00bb\b\3\3\2\u00bb")
        buf.write("\t\3\2\2\2\u00bc\u00bd\7>\2\2\u00bd\u00be\7A\2\2\u00be")
        buf.write("\u00bf\3\2\2\2\u00bf\u00c0\b\4\4\2\u00c0\13\3\2\2\2\u00c1")
        buf.write("\u00c3\13\2\2\2\u00c2\u00c1\3\2\2\2\u00c3\u00c4\3\2\2")
        buf.write("\2\u00c4\u00c5\3\2\2\2\u00c4\u00c2\3\2\2\2\u00c5\r\3\2")
        buf.write("\2\2\u00c6\u00c7\7>\2\2\u00c7\u00c8\7A\2\2\u00c8\u00c9")
        buf.write("\3\2\2\2\u00c9\u00ca\b\6\4\2\u00ca\17\3\2\2\2\u00cb\u00cd")
        buf.write("\13\2\2\2\u00cc\u00cb\3\2\2\2\u00cd\u00ce\3\2\2\2\u00ce")
        buf.write("\u00cf\3\2\2\2\u00ce\u00cc\3\2\2\2\u00cf\21\3\2\2\2\u00d0")
        buf.write("\u00d2\t\3\2\2\u00d1\u00d0\3\2\2\2\u00d2\u00d3\3\2\2\2")
        buf.write("\u00d3\u00d1\3\2\2\2\u00d3\u00d4\3\2\2\2\u00d4\23\3\2")
        buf.write("\2\2\u00d5\u00d6\7y\2\2\u00d6\u00d7\7j\2\2\u00d7\u00d8")
        buf.write("\7k\2\2\u00d8\u00d9\7v\2\2\u00d9\u00da\7g\2\2\u00da\u00db")
        buf.write("\7u\2\2\u00db\u00dc\7r\2\2\u00dc\u00dd\7c\2\2\u00dd\u00de")
        buf.write("\7e\2\2\u00de\u00df\7g\2\2\u00df\25\3\2\2\2\u00e0\u00e1")
        buf.write("\7f\2\2\u00e1\u00e2\7q\2\2\u00e2\u00e3\7e\2\2\u00e3\27")
        buf.write("\3\2\2\2\u00e4\u00e5\7p\2\2\u00e5\u00e6\7q\2\2\u00e6\u00e7")
        buf.write("\7v\2\2\u00e7\u00e8\7g\2\2\u00e8\31\3\2\2\2\u00e9\u00ea")
        buf.write("\7w\2\2\u00ea\u00eb\7n\2\2\u00eb\u00ec\7\66\2\2\u00ec")
        buf.write("\33\3\2\2\2\u00ed\u00ee\7f\2\2\u00ee\u00ef\7g\2\2\u00ef")
        buf.write("\u00f0\7h\2\2\u00f0\35\3\2\2\2\u00f1\u00f2\7h\2\2\u00f2")
        buf.write("\u00f3\7q\2\2\u00f3\u00f4\7t\2\2\u00f4\37\3\2\2\2\u00f5")
        buf.write("\u00f6\7y\2\2\u00f6\u00f7\7j\2\2\u00f7\u00f8\7k\2\2\u00f8")
        buf.write("\u00f9\7n\2\2\u00f9\u00fa\7g\2\2\u00fa!\3\2\2\2\u00fb")
        buf.write("\u00fc\7k\2\2\u00fc\u00fd\7h\2\2\u00fd#\3\2\2\2\u00fe")
        buf.write("\u00ff\7g\2\2\u00ff\u0100\7n\2\2\u0100\u0101\7k\2\2\u0101")
        buf.write("\u0102\7h\2\2\u0102%\3\2\2\2\u0103\u0104\7g\2\2\u0104")
        buf.write("\u0105\7n\2\2\u0105\u0106\7u\2\2\u0106\u0107\7g\2\2\u0107")
        buf.write("\'\3\2\2\2\u0108\u0109\7t\2\2\u0109\u010a\7g\2\2\u010a")
        buf.write("\u010b\7p\2\2\u010b\u010c\7f\2\2\u010c\u010d\7g\2\2\u010d")
        buf.write("\u010e\7t\2\2\u010e\u010f\7d\2\2\u010f\u0110\7n\2\2\u0110")
        buf.write("\u0111\7q\2\2\u0111\u0112\7e\2\2\u0112\u0113\7m\2\2\u0113")
        buf.write(")\3\2\2\2\u0114\u0115\7t\2\2\u0115\u0116\7g\2\2\u0116")
        buf.write("\u0117\7p\2\2\u0117\u0118\7f\2\2\u0118\u0119\7g\2\2\u0119")
        buf.write("\u011a\7t\2\2\u011a\u011b\7d\2\2\u011b\u011c\7n\2\2\u011c")
        buf.write("\u011d\7q\2\2\u011d\u011e\7e\2\2\u011e\u011f\7m\2\2\u011f")
        buf.write("\u0120\7u\2\2\u0120+\3\2\2\2\u0121\u0122\7g\2\2\u0122")
        buf.write("\u0123\7p\2\2\u0123\u0124\7f\2\2\u0124-\3\2\2\2\u0125")
        buf.write("\u0127\13\2\2\2\u0126\u0125\3\2\2\2\u0127\u0128\3\2\2")
        buf.write("\2\u0128\u0129\3\2\2\2\u0128\u0126\3\2\2\2\u0129/\3\2")
        buf.write("\2\2\u012a\u012b\7A\2\2\u012b\u012c\7@\2\2\u012c\61\3")
        buf.write("\2\2\2\u012d\u012e\7h\2\2\u012e\u012f\7q\2\2\u012f\u0130")
        buf.write("\7t\2\2\u0130\63\3\2\2\2\u0131\u0132\7k\2\2\u0132\u0133")
        buf.write("\7p\2\2\u0133\65\3\2\2\2\u0134\u0135\7k\2\2\u0135\u0136")
        buf.write("\7h\2\2\u0136\67\3\2\2\2\u0137\u0138\7g\2\2\u0138\u0139")
        buf.write("\7n\2\2\u0139\u013a\7u\2\2\u013a\u013b\7g\2\2\u013b9\3")
        buf.write("\2\2\2\u013c\u013d\7p\2\2\u013d\u013e\7q\2\2\u013e\u013f")
        buf.write("\7v\2\2\u013f;\3\2\2\2\u0140\u0141\7k\2\2\u0141\u0142")
        buf.write("\7u\2\2\u0142=\3\2\2\2\u0143\u0144\7c\2\2\u0144\u0145")
        buf.write("\7p\2\2\u0145\u0146\7f\2\2\u0146?\3\2\2\2\u0147\u0148")
        buf.write("\7q\2\2\u0148\u0149\7t\2\2\u0149A\3\2\2\2\u014a\u014b")
        buf.write("\7P\2\2\u014b\u014c\7q\2\2\u014c\u014d\7p\2\2\u014d\u014e")
        buf.write("\7g\2\2\u014eC\3\2\2\2\u014f\u0150\7V\2\2\u0150\u0151")
        buf.write("\7t\2\2\u0151\u0152\7w\2\2\u0152\u0153\7g\2\2\u0153E\3")
        buf.write("\2\2\2\u0154\u0155\7H\2\2\u0155\u0156\7c\2\2\u0156\u0157")
        buf.write("\7n\2\2\u0157\u0158\7u\2\2\u0158\u0159\7g\2\2\u0159G\3")
        buf.write("\2\2\2\u015a\u015b\7f\2\2\u015b\u015c\7g\2\2\u015c\u015d")
        buf.write("\7h\2\2\u015dI\3\2\2\2\u015e\u015f\7y\2\2\u015f\u0160")
        buf.write("\7j\2\2\u0160\u0161\7k\2\2\u0161\u0162\7n\2\2\u0162\u0163")
        buf.write("\7g\2\2\u0163K\3\2\2\2\u0164\u0165\7t\2\2\u0165\u0166")
        buf.write("\7g\2\2\u0166\u0167\7p\2\2\u0167\u0168\7f\2\2\u0168\u0169")
        buf.write("\7g\2\2\u0169\u016a\7t\2\2\u016a\u016b\7d\2\2\u016b\u016c")
        buf.write("\7n\2\2\u016c\u016d\7q\2\2\u016d\u016e\7e\2\2\u016e\u016f")
        buf.write("\7m\2\2\u016fM\3\2\2\2\u0170\u0171\7t\2\2\u0171\u0172")
        buf.write("\7g\2\2\u0172\u0173\7p\2\2\u0173\u0174\7f\2\2\u0174\u0175")
        buf.write("\7g\2\2\u0175\u0176\7t\2\2\u0176\u0177\7d\2\2\u0177\u0178")
        buf.write("\7n\2\2\u0178\u0179\7q\2\2\u0179\u017a\7e\2\2\u017a\u017b")
        buf.write("\7m\2\2\u017b\u017c\7u\2\2\u017cO\3\2\2\2\u017d\u017e")
        buf.write("\7*\2\2\u017eQ\3\2\2\2\u017f\u0180\7+\2\2\u0180S\3\2\2")
        buf.write("\2\u0181\u0182\7]\2\2\u0182U\3\2\2\2\u0183\u0184\7_\2")
        buf.write("\2\u0184W\3\2\2\2\u0185\u0186\7}\2\2\u0186Y\3\2\2\2\u0187")
        buf.write("\u0188\7\177\2\2\u0188[\3\2\2\2\u0189\u018a\7,\2\2\u018a")
        buf.write("\u018b\7,\2\2\u018b]\3\2\2\2\u018c\u018d\7,\2\2\u018d")
        buf.write("_\3\2\2\2\u018e\u018f\7-\2\2\u018fa\3\2\2\2\u0190\u0191")
        buf.write("\7/\2\2\u0191c\3\2\2\2\u0192\u0193\7\61\2\2\u0193\u0194")
        buf.write("\7\61\2\2\u0194e\3\2\2\2\u0195\u0196\7\61\2\2\u0196g\3")
        buf.write("\2\2\2\u0197\u0198\7\'\2\2\u0198i\3\2\2\2\u0199\u019a")
        buf.write("\7?\2\2\u019a\u019b\7?\2\2\u019bk\3\2\2\2\u019c\u019d")
        buf.write("\7#\2\2\u019d\u019e\7?\2\2\u019em\3\2\2\2\u019f\u01a0")
        buf.write("\7>\2\2\u01a0\u01a1\7?\2\2\u01a1o\3\2\2\2\u01a2\u01a3")
        buf.write("\7>\2\2\u01a3q\3\2\2\2\u01a4\u01a5\7@\2\2\u01a5\u01a6")
        buf.write("\7?\2\2\u01a6s\3\2\2\2\u01a7\u01a8\7@\2\2\u01a8u\3\2\2")
        buf.write("\2\u01a9\u01aa\7?\2\2\u01aaw\3\2\2\2\u01ab\u01ac\7.\2")
        buf.write("\2\u01acy\3\2\2\2\u01ad\u01ae\7<\2\2\u01ae{\3\2\2\2\u01af")
        buf.write("\u01b0\7\u0080\2\2\u01b0}\3\2\2\2\u01b1\u01b2\7(\2\2\u01b2")
        buf.write("\177\3\2\2\2\u01b3\u01b4\7`\2\2\u01b4\u0081\3\2\2\2\u01b5")
        buf.write("\u01b6\7\60\2\2\u01b6\u0083\3\2\2\2\u01b7\u01bb\t\4\2")
        buf.write("\2\u01b8\u01ba\t\5\2\2\u01b9\u01b8\3\2\2\2\u01ba\u01bd")
        buf.write("\3\2\2\2\u01bb\u01b9\3\2\2\2\u01bb\u01bc\3\2\2\2\u01bc")
        buf.write("\u0085\3\2\2\2\u01bd\u01bb\3\2\2\2\u01be\u01bf\4\62;\2")
        buf.write("\u01bf\u0087\3\2\2\2\u01c0\u01c1\4\62\63\2\u01c1\u0089")
        buf.write("\3\2\2\2\u01c2\u01c3\4\629\2\u01c3\u008b\3\2\2\2\u01c4")
        buf.write("\u01c5\t\6\2\2\u01c5\u008d\3\2\2\2\u01c6\u01c8\5\u0086")
        buf.write("B\2\u01c7\u01c6\3\2\2\2\u01c8\u01c9\3\2\2\2\u01c9\u01c7")
        buf.write("\3\2\2\2\u01c9\u01ca\3\2\2\2\u01ca\u01e1\3\2\2\2\u01cb")
        buf.write("\u01cc\7\62\2\2\u01cc\u01ce\t\7\2\2\u01cd\u01cf\5\u0088")
        buf.write("C\2\u01ce\u01cd\3\2\2\2\u01cf\u01d0\3\2\2\2\u01d0\u01ce")
        buf.write("\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1\u01e1\3\2\2\2\u01d2")
        buf.write("\u01d3\7\62\2\2\u01d3\u01d5\t\b\2\2\u01d4\u01d6\5\u008a")
        buf.write("D\2\u01d5\u01d4\3\2\2\2\u01d6\u01d7\3\2\2\2\u01d7\u01d5")
        buf.write("\3\2\2\2\u01d7\u01d8\3\2\2\2\u01d8\u01e1\3\2\2\2\u01d9")
        buf.write("\u01da\7\62\2\2\u01da\u01dc\t\t\2\2\u01db\u01dd\5\u008c")
        buf.write("E\2\u01dc\u01db\3\2\2\2\u01dd\u01de\3\2\2\2\u01de\u01dc")
        buf.write("\3\2\2\2\u01de\u01df\3\2\2\2\u01df\u01e1\3\2\2\2\u01e0")
        buf.write("\u01c7\3\2\2\2\u01e0\u01cb\3\2\2\2\u01e0\u01d2\3\2\2\2")
        buf.write("\u01e0\u01d9\3\2\2\2\u01e1\u008f\3\2\2\2\u01e2\u01e4\t")
        buf.write("\n\2\2\u01e3\u01e5\t\13\2\2\u01e4\u01e3\3\2\2\2\u01e4")
        buf.write("\u01e5\3\2\2\2\u01e5\u01e7\3\2\2\2\u01e6\u01e8\5\u0086")
        buf.write("B\2\u01e7\u01e6\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9\u01e7")
        buf.write("\3\2\2\2\u01e9\u01ea\3\2\2\2\u01ea\u0091\3\2\2\2\u01eb")
        buf.write("\u01ed\5\u0086B\2\u01ec\u01eb\3\2\2\2\u01ed\u01ee\3\2")
        buf.write("\2\2\u01ee\u01ec\3\2\2\2\u01ee\u01ef\3\2\2\2\u01ef\u01f0")
        buf.write("\3\2\2\2\u01f0\u01f4\7\60\2\2\u01f1\u01f3\5\u0086B\2\u01f2")
        buf.write("\u01f1\3\2\2\2\u01f3\u01f6\3\2\2\2\u01f4\u01f2\3\2\2\2")
        buf.write("\u01f4\u01f5\3\2\2\2\u01f5\u01f8\3\2\2\2\u01f6\u01f4\3")
        buf.write("\2\2\2\u01f7\u01f9\5\u0090G\2\u01f8\u01f7\3\2\2\2\u01f8")
        buf.write("\u01f9\3\2\2\2\u01f9\u020b\3\2\2\2\u01fa\u01fc\7\60\2")
        buf.write("\2\u01fb\u01fd\5\u0086B\2\u01fc\u01fb\3\2\2\2\u01fd\u01fe")
        buf.write("\3\2\2\2\u01fe\u01fc\3\2\2\2\u01fe\u01ff\3\2\2\2\u01ff")
        buf.write("\u0201\3\2\2\2\u0200\u0202\5\u0090G\2\u0201\u0200\3\2")
        buf.write("\2\2\u0201\u0202\3\2\2\2\u0202\u020b\3\2\2\2\u0203\u0205")
        buf.write("\5\u0086B\2\u0204\u0203\3\2\2\2\u0205\u0206\3\2\2\2\u0206")
        buf.write("\u0204\3\2\2\2\u0206\u0207\3\2\2\2\u0207\u0208\3\2\2\2")
        buf.write("\u0208\u0209\5\u0090G\2\u0209\u020b\3\2\2\2\u020a\u01ec")
        buf.write("\3\2\2\2\u020a\u01fa\3\2\2\2\u020a\u0204\3\2\2\2\u020b")
        buf.write("\u0093\3\2\2\2\u020c\u020d\5\u0086B\2\u020d\u020e\5\u0086")
        buf.write("B\2\u020e\u020f\7<\2\2\u020f\u0210\5\u0086B\2\u0210\u021e")
        buf.write("\5\u0086B\2\u0211\u0212\7<\2\2\u0212\u0213\5\u0086B\2")
        buf.write("\u0213\u021c\5\u0086B\2\u0214\u0215\7\60\2\2\u0215\u0216")
        buf.write("\5\u0086B\2\u0216\u0217\5\u0086B\2\u0217\u0218\5\u0086")
        buf.write("B\2\u0218\u0219\5\u0086B\2\u0219\u021a\5\u0086B\2\u021a")
        buf.write("\u021b\5\u0086B\2\u021b\u021d\3\2\2\2\u021c\u0214\3\2")
        buf.write("\2\2\u021c\u021d\3\2\2\2\u021d\u021f\3\2\2\2\u021e\u0211")
        buf.write("\3\2\2\2\u021e\u021f\3\2\2\2\u021f\u0095\3\2\2\2\u0220")
        buf.write("\u0221\7B\2\2\u0221\u0222\7*\2\2\u0222\u0223\5\u0086B")
        buf.write("\2\u0223\u0224\5\u0086B\2\u0224\u0225\5\u0086B\2\u0225")
        buf.write("\u0226\5\u0086B\2\u0226\u0227\7/\2\2\u0227\u0228\5\u0086")
        buf.write("B\2\u0228\u0229\5\u0086B\2\u0229\u022a\7/\2\2\u022a\u022b")
        buf.write("\5\u0086B\2\u022b\u022c\5\u0086B\2\u022c\u022d\7+\2\2")
        buf.write("\u022d\u0097\3\2\2\2\u022e\u022f\7B\2\2\u022f\u0230\7")
        buf.write("*\2\2\u0230\u0231\5\u0086B\2\u0231\u0232\5\u0086B\2\u0232")
        buf.write("\u0233\5\u0086B\2\u0233\u0234\5\u0086B\2\u0234\u0235\7")
        buf.write("/\2\2\u0235\u0236\5\u0086B\2\u0236\u0237\5\u0086B\2\u0237")
        buf.write("\u0238\7/\2\2\u0238\u0239\5\u0086B\2\u0239\u023a\5\u0086")
        buf.write("B\2\u023a\u023c\7V\2\2\u023b\u023d\5\u0094I\2\u023c\u023b")
        buf.write("\3\2\2\2\u023c\u023d\3\2\2\2\u023d\u023e\3\2\2\2\u023e")
        buf.write("\u023f\7+\2\2\u023f\u0099\3\2\2\2\u0240\u0241\7%\2\2\u0241")
        buf.write("\u0242\5\u008cE\2\u0242\u0243\5\u008cE\2\u0243\u0244\5")
        buf.write("\u008cE\2\u0244\u025e\3\2\2\2\u0245\u0246\7%\2\2\u0246")
        buf.write("\u0247\5\u008cE\2\u0247\u0248\5\u008cE\2\u0248\u0249\5")
        buf.write("\u008cE\2\u0249\u024a\5\u008cE\2\u024a\u025e\3\2\2\2\u024b")
        buf.write("\u024c\7%\2\2\u024c\u024d\5\u008cE\2\u024d\u024e\5\u008c")
        buf.write("E\2\u024e\u024f\5\u008cE\2\u024f\u0250\5\u008cE\2\u0250")
        buf.write("\u0251\5\u008cE\2\u0251\u0252\5\u008cE\2\u0252\u025e\3")
        buf.write("\2\2\2\u0253\u0254\7%\2\2\u0254\u0255\5\u008cE\2\u0255")
        buf.write("\u0256\5\u008cE\2\u0256\u0257\5\u008cE\2\u0257\u0258\5")
        buf.write("\u008cE\2\u0258\u0259\5\u008cE\2\u0259\u025a\5\u008cE")
        buf.write("\2\u025a\u025b\5\u008cE\2\u025b\u025c\5\u008cE\2\u025c")
        buf.write("\u025e\3\2\2\2\u025d\u0240\3\2\2\2\u025d\u0245\3\2\2\2")
        buf.write("\u025d\u024b\3\2\2\2\u025d\u0253\3\2\2\2\u025e\u009b\3")
        buf.write("\2\2\2\u025f\u0260\t\3\2\2\u0260\u0261\3\2\2\2\u0261\u0262")
        buf.write("\bM\5\2\u0262\u009d\3\2\2\2\u0263\u0268\7$\2\2\u0264\u0267")
        buf.write("\5\u00a6R\2\u0265\u0267\n\f\2\2\u0266\u0264\3\2\2\2\u0266")
        buf.write("\u0265\3\2\2\2\u0267\u026a\3\2\2\2\u0268\u0266\3\2\2\2")
        buf.write("\u0268\u0269\3\2\2\2\u0269\u026b\3\2\2\2\u026a\u0268\3")
        buf.write("\2\2\2\u026b\u0276\7$\2\2\u026c\u0271\7)\2\2\u026d\u0270")
        buf.write("\5\u00a6R\2\u026e\u0270\n\r\2\2\u026f\u026d\3\2\2\2\u026f")
        buf.write("\u026e\3\2\2\2\u0270\u0273\3\2\2\2\u0271\u026f\3\2\2\2")
        buf.write("\u0271\u0272\3\2\2\2\u0272\u0274\3\2\2\2\u0273\u0271\3")
        buf.write("\2\2\2\u0274\u0276\7)\2\2\u0275\u0263\3\2\2\2\u0275\u026c")
        buf.write("\3\2\2\2\u0276\u009f\3\2\2\2\u0277\u0278\7$\2\2\u0278")
        buf.write("\u0279\7$\2\2\u0279\u027a\7$\2\2\u027a\u027e\3\2\2\2\u027b")
        buf.write("\u027d\5\u00a2P\2\u027c\u027b\3\2\2\2\u027d\u0280\3\2")
        buf.write("\2\2\u027e\u027f\3\2\2\2\u027e\u027c\3\2\2\2\u027f\u0281")
        buf.write("\3\2\2\2\u0280\u027e\3\2\2\2\u0281\u0282\7$\2\2\u0282")
        buf.write("\u0283\7$\2\2\u0283\u0292\7$\2\2\u0284\u0285\7)\2\2\u0285")
        buf.write("\u0286\7)\2\2\u0286\u0287\7)\2\2\u0287\u028b\3\2\2\2\u0288")
        buf.write("\u028a\5\u00a4Q\2\u0289\u0288\3\2\2\2\u028a\u028d\3\2")
        buf.write("\2\2\u028b\u028c\3\2\2\2\u028b\u0289\3\2\2\2\u028c\u028e")
        buf.write("\3\2\2\2\u028d\u028b\3\2\2\2\u028e\u028f\7)\2\2\u028f")
        buf.write("\u0290\7)\2\2\u0290\u0292\7)\2\2\u0291\u0277\3\2\2\2\u0291")
        buf.write("\u0284\3\2\2\2\u0292\u00a1\3\2\2\2\u0293\u0297\7$\2\2")
        buf.write("\u0294\u0295\7$\2\2\u0295\u0297\7$\2\2\u0296\u0293\3\2")
        buf.write("\2\2\u0296\u0294\3\2\2\2\u0296\u0297\3\2\2\2\u0297\u029a")
        buf.write("\3\2\2\2\u0298\u029b\5\u00a6R\2\u0299\u029b\n\16\2\2\u029a")
        buf.write("\u0298\3\2\2\2\u029a\u0299\3\2\2\2\u029b\u029c\3\2\2\2")
        buf.write("\u029c\u029a\3\2\2\2\u029c\u029d\3\2\2\2\u029d\u00a3\3")
        buf.write("\2\2\2\u029e\u02a2\7)\2\2\u029f\u02a0\7)\2\2\u02a0\u02a2")
        buf.write("\7)\2\2\u02a1\u029e\3\2\2\2\u02a1\u029f\3\2\2\2\u02a1")
        buf.write("\u02a2\3\2\2\2\u02a2\u02a5\3\2\2\2\u02a3\u02a6\5\u00a6")
        buf.write("R\2\u02a4\u02a6\n\17\2\2\u02a5\u02a3\3\2\2\2\u02a5\u02a4")
        buf.write("\3\2\2\2\u02a6\u02a7\3\2\2\2\u02a7\u02a5\3\2\2\2\u02a7")
        buf.write("\u02a8\3\2\2\2\u02a8\u00a5\3\2\2\2\u02a9\u02aa\7^\2\2")
        buf.write("\u02aa\u02af\t\20\2\2\u02ab\u02af\5\u00a8S\2\u02ac\u02af")
        buf.write("\5\u00aaT\2\u02ad\u02af\5\u00acU\2\u02ae\u02a9\3\2\2\2")
        buf.write("\u02ae\u02ab\3\2\2\2\u02ae\u02ac\3\2\2\2\u02ae\u02ad\3")
        buf.write("\2\2\2\u02af\u00a7\3\2\2\2\u02b0\u02b1\7^\2\2\u02b1\u02b2")
        buf.write("\7z\2\2\u02b2\u02b3\5\u008cE\2\u02b3\u02b4\5\u008cE\2")
        buf.write("\u02b4\u00a9\3\2\2\2\u02b5\u02b6\7^\2\2\u02b6\u02b7\7")
        buf.write("w\2\2\u02b7\u02b8\5\u008cE\2\u02b8\u02b9\5\u008cE\2\u02b9")
        buf.write("\u02ba\5\u008cE\2\u02ba\u02bb\5\u008cE\2\u02bb\u00ab\3")
        buf.write("\2\2\2\u02bc\u02bd\7^\2\2\u02bd\u02be\7W\2\2\u02be\u02bf")
        buf.write("\5\u008cE\2\u02bf\u02c0\5\u008cE\2\u02c0\u02c1\5\u008c")
        buf.write("E\2\u02c1\u02c2\5\u008cE\2\u02c2\u02c3\5\u008cE\2\u02c3")
        buf.write("\u02c4\5\u008cE\2\u02c4\u02c5\5\u008cE\2\u02c5\u02c6\5")
        buf.write("\u008cE\2\u02c6\u00ad\3\2\2\2.\2\3\4\5\u00b1\u00b6\u00c4")
        buf.write("\u00ce\u00d3\u0128\u01bb\u01c9\u01d0\u01d7\u01de\u01e0")
        buf.write("\u01e4\u01e9\u01ee\u01f4\u01f8\u01fe\u0201\u0206\u020a")
        buf.write("\u021c\u021e\u023c\u025d\u0266\u0268\u026f\u0271\u0275")
        buf.write("\u027e\u028b\u0291\u0296\u029a\u029c\u02a1\u02a5\u02a7")
        buf.write("\u02ae\6\7\3\2\4\2\2\7\4\2\b\2\2")
        return buf.getvalue()


class UL4_Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    TEXT_MODE = 1
    MAYBETAG_MODE = 2
    TAG_MODE = 3

    DEFAULT_INDENT = 1
    DEFAULT_LINEEND = 2
    DEFAULT_MAYBETAG = 3
    DEFAULT_TEXT = 4
    TEXT_MAYBETAG = 5
    TEXT_TEXT = 6
    MAYBETAG_WS = 7
    MAYBETAG_WHITESPACE = 8
    MAYBETAG_DOC = 9
    MAYBETAG_NOTE = 10
    MAYBETAG_UL4 = 11
    MAYBETAG_DEF = 12
    MAYBETAG_FOR = 13
    MAYBETAG_WHILE = 14
    MAYBETAG_IF = 15
    MAYBETAG_ELIF = 16
    MAYBETAG_ELSE = 17
    MAYBETAG_RENDERBLOCK = 18
    MAYBETAG_RENDERBLOCKS = 19
    MAYBETAG_END = 20
    MAYBETAG_OTHER = 21
    ENDDELIM = 22
    FOR = 23
    IN = 24
    IF = 25
    ELSE = 26
    NOT = 27
    IS = 28
    AND = 29
    OR = 30
    NONE = 31
    TRUE = 32
    FALSE = 33
    DEF = 34
    WHILE = 35
    RENDERBLOCK = 36
    RENDERBLOCKS = 37
    PARENS_OPEN = 38
    PARENS_CLOSE = 39
    BRACKET_OPEN = 40
    BRACKET_CLOSE = 41
    BRACE_OPEN = 42
    BRACE_CLOSE = 43
    STAR_STAR = 44
    STAR = 45
    PLUS = 46
    MINUS = 47
    SLASH_SLASH = 48
    SLASH = 49
    PERCENT = 50
    EQUAL = 51
    NOT_EQUAL = 52
    LESS_THAN_OR_EQUAL = 53
    LESS_THAN = 54
    GREATER_THAN_OR_EQUAL = 55
    GREATER_THAN = 56
    ASSIGN = 57
    COMMA = 58
    COLON = 59
    TILDE = 60
    AMPERSAND = 61
    CARET = 62
    DOT = 63
    NAME = 64
    INT = 65
    FLOAT = 66
    DATE = 67
    DATETIME = 68
    COLOR = 69
    WS = 70
    STRING = 71
    STRING3 = 72

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE", "TEXT_MODE", "MAYBETAG_MODE", "TAG_MODE" ]

    literalNames = [ "<INVALID>",
            "'whitespace'", "'doc'", "'note'", "'ul4'", "'elif'", "'end'", 
            "'?>'", "'in'", "'not'", "'is'", "'and'", "'or'", "'None'", 
            "'True'", "'False'", "'('", "')'", "'['", "']'", "'{'", "'}'", 
            "'**'", "'*'", "'+'", "'-'", "'//'", "'/'", "'%'", "'=='", "'!='", 
            "'<='", "'<'", "'>='", "'>'", "'='", "','", "':'", "'~'", "'&'", 
            "'^'", "'.'" ]

    symbolicNames = [ "<INVALID>",
            "DEFAULT_INDENT", "DEFAULT_LINEEND", "DEFAULT_MAYBETAG", "DEFAULT_TEXT", 
            "TEXT_MAYBETAG", "TEXT_TEXT", "MAYBETAG_WS", "MAYBETAG_WHITESPACE", 
            "MAYBETAG_DOC", "MAYBETAG_NOTE", "MAYBETAG_UL4", "MAYBETAG_DEF", 
            "MAYBETAG_FOR", "MAYBETAG_WHILE", "MAYBETAG_IF", "MAYBETAG_ELIF", 
            "MAYBETAG_ELSE", "MAYBETAG_RENDERBLOCK", "MAYBETAG_RENDERBLOCKS", 
            "MAYBETAG_END", "MAYBETAG_OTHER", "ENDDELIM", "FOR", "IN", "IF", 
            "ELSE", "NOT", "IS", "AND", "OR", "NONE", "TRUE", "FALSE", "DEF", 
            "WHILE", "RENDERBLOCK", "RENDERBLOCKS", "PARENS_OPEN", "PARENS_CLOSE", 
            "BRACKET_OPEN", "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", 
            "STAR_STAR", "STAR", "PLUS", "MINUS", "SLASH_SLASH", "SLASH", 
            "PERCENT", "EQUAL", "NOT_EQUAL", "LESS_THAN_OR_EQUAL", "LESS_THAN", 
            "GREATER_THAN_OR_EQUAL", "GREATER_THAN", "ASSIGN", "COMMA", 
            "COLON", "TILDE", "AMPERSAND", "CARET", "DOT", "NAME", "INT", 
            "FLOAT", "DATE", "DATETIME", "COLOR", "WS", "STRING", "STRING3" ]

    ruleNames = [ "DEFAULT_INDENT", "DEFAULT_LINEEND", "DEFAULT_MAYBETAG", 
                  "DEFAULT_TEXT", "TEXT_MAYBETAG", "TEXT_TEXT", "MAYBETAG_WS", 
                  "MAYBETAG_WHITESPACE", "MAYBETAG_DOC", "MAYBETAG_NOTE", 
                  "MAYBETAG_UL4", "MAYBETAG_DEF", "MAYBETAG_FOR", "MAYBETAG_WHILE", 
                  "MAYBETAG_IF", "MAYBETAG_ELIF", "MAYBETAG_ELSE", "MAYBETAG_RENDERBLOCK", 
                  "MAYBETAG_RENDERBLOCKS", "MAYBETAG_END", "MAYBETAG_OTHER", 
                  "ENDDELIM", "FOR", "IN", "IF", "ELSE", "NOT", "IS", "AND", 
                  "OR", "NONE", "TRUE", "FALSE", "DEF", "WHILE", "RENDERBLOCK", 
                  "RENDERBLOCKS", "PARENS_OPEN", "PARENS_CLOSE", "BRACKET_OPEN", 
                  "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", "STAR_STAR", 
                  "STAR", "PLUS", "MINUS", "SLASH_SLASH", "SLASH", "PERCENT", 
                  "EQUAL", "NOT_EQUAL", "LESS_THAN_OR_EQUAL", "LESS_THAN", 
                  "GREATER_THAN_OR_EQUAL", "GREATER_THAN", "ASSIGN", "COMMA", 
                  "COLON", "TILDE", "AMPERSAND", "CARET", "DOT", "NAME", 
                  "DIGIT", "BIN_DIGIT", "OCT_DIGIT", "HEX_DIGIT", "INT", 
                  "EXPONENT", "FLOAT", "TIME", "DATE", "DATETIME", "COLOR", 
                  "WS", "STRING", "STRING3", "TRIQUOTE", "TRIAPOS", "ESC_SEQ", 
                  "UNICODE1_ESC", "UNICODE2_ESC", "UNICODE4_ESC" ]

    grammarFileName = "UL4_Lexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


