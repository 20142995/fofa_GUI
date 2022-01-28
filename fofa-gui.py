#-*- coding:utf-8 -*-
import base64
import configparser
import os
import requests
import sys
import threading
import time
import xlsxwriter
from tkinter import *
from tkinter . font import Font
from tkinter . messagebox import *
from tkinter . ttk import *
def I1IiI ( _file ) :
 o0OOO = { }
 iIiiiI = configparser . ConfigParser ( )
 iIiiiI . read ( _file , encoding = "utf-8" )
 Iii1ii1II11i = iIiiiI . sections ( )
 for iI111iI in Iii1ii1II11i :
  o0OOO . setdefault ( iI111iI , { } )
  o0OOO [ iI111iI ] . update ( dict ( iIiiiI . items ( iI111iI ) ) )
 return o0OOO
def Oo ( excle_name , ** tables ) :
 I1Ii11I1Ii1i = xlsxwriter . Workbook ( excle_name )
 for Ooo , o0oOoO00o in tables . items ( ) :
  if not o0oOoO00o : continue
  i1 = I1Ii11I1Ii1i . add_worksheet ( Ooo )
  for oOOoo00O0O , i1111 in enumerate ( o0oOoO00o ) :
   i1 . write_row ( oOOoo00O0O , 0 , i1111 )
 I1Ii11I1Ii1i . close ( )
def Iiii ( excle_name , ** tables ) :
 OOO0O = { }
 for Ooo in tables :
  OOO0O . setdefault ( Ooo , [ ] )
  for iI111iI in tables [ Ooo ] :
   for oo0ooO0oOOOOo in iI111iI . keys ( ) :
    if oo0ooO0oOOOOo not in OOO0O [ Ooo ] :
     OOO0O [ Ooo ] . append ( oo0ooO0oOOOOo )
 o0OOO = { }
 for Ooo in tables :
  o0OOO . setdefault ( Ooo , [ OOO0O [ Ooo ] ] )
  for iI111iI in tables [ Ooo ] :
   i1111 = [ ]
   for oo0ooO0oOOOOo in OOO0O [ Ooo ] :
    i1111 . append ( iI111iI . get ( oo0ooO0oOOOOo , '' ) )
   o0OOO [ Ooo ] . append ( i1111 )
 Oo ( excle_name , ** o0OOO )
global O0OoOoo00o
O0OoOoo00o = False
IiiIII111ii = I1IiI ( 'config.ini' )
I1Ii = IiiIII111ii [ 'fofa' ] [ 'email' ]
o0oOo0Ooo0O = IiiIII111ii [ 'fofa' ] [ 'key' ]
class OooO0OO ( Frame ) :
 def __init__ ( self , master = None ) :
  Frame . __init__ ( self , master )
  self . master . title ( 'Fofa 查询小工具 by:20142995' )
  self . master . geometry ( '701x463' )
  self . createWidgets ( )
 def createWidgets ( self ) :
  self . top = self . winfo_toplevel ( )
  self . style = Style ( )
  self . style . configure ( 'Label1.TLabel' , anchor = 'w' , font = ( '宋体' , 9 ) )
  self . Label1 = Label ( self . top , text = '查询语句：' , style = 'Label1.TLabel' )
  self . Label1 . place ( relx = 0.011 , rely = 0.017 , relwidth = 0.093 , relheight = 0.037 )
  self . Text_queryFont = Font ( font = ( '宋体' , 9 ) )
  self . Text_query = Text ( self . top , font = self . Text_queryFont )
  self . Text_query . place ( relx = 0.011 , rely = 0.086 , relwidth = 0.515 , relheight = 0.434 )
  self . style . configure ( 'Label2.TLabel' , anchor = 'w' , font = ( '宋体' , 9 ) )
  self . Label2 = Label ( self . top , text = '日志：' , style = 'Label2.TLabel' )
  self . Label2 . place ( relx = 0.023 , rely = 0.553 , relwidth = 0.104 , relheight = 0.037 )
  self . Text_outFont = Font ( font = ( '宋体' , 9 ) )
  self . Text_out = Text ( self . top , font = self . Text_outFont )
  self . Text_out . place ( relx = 0.011 , rely = 0.622 , relwidth = 0.515 , relheight = 0.313 )
  self . style . configure ( 'Command_query.TButton' , font = ( '宋体' , 9 ) )
  self . Command_query = Button ( self . top , text = '查询' , command = self . Command_query_Cmd , style = 'Command_query.TButton' )
  self . Command_query . place ( relx = 0.605 , rely = 0.76 , relwidth = 0.127 , relheight = 0.071 )
  self . style . configure ( 'Label3.TLabel' , anchor = 'w' , font = ( '宋体' , 9 ) )
  self . Label3 = Label ( self . top , text = '每页' , style = 'Label3.TLabel' )
  self . Label3 . place ( relx = 0.582 , rely = 0.035 , relwidth = 0.047 , relheight = 0.037 )
  self . style . configure ( 'Label4.TLabel' , anchor = 'w' , font = ( '宋体' , 9 ) )
  self . Label4 = Label ( self . top , text = '最大' , style = 'Label4.TLabel' )
  self . Label4 . place ( relx = 0.776 , rely = 0.035 , relwidth = 0.058 , relheight = 0.037 )
  self . style . configure ( 'Label5.TLabel' , anchor = 'w' , font = ( '宋体' , 9 ) )
  self . Label5 = Label ( self . top , text = '条' , style = 'Label5.TLabel' )
  self . Label5 . place ( relx = 0.719 , rely = 0.035 , relwidth = 0.047 , relheight = 0.037 )
  self . style . configure ( 'Label6.TLabel' , anchor = 'w' , font = ( '宋体' , 9 ) )
  self . Label6 = Label ( self . top , text = '页' , style = 'Label6.TLabel' )
  self . Label6 . place ( relx = 0.89 , rely = 0.035 , relwidth = 0.036 , relheight = 0.037 )
  self . Text_sizeVar = StringVar ( value = '100' )
  self . Text_size = Entry ( self . top , text = '100' , textvariable = self . Text_sizeVar , font = ( '宋体' , 9 ) )
  self . Text_size . place ( relx = 0.628 , rely = 0.017 , relwidth = 0.07 , relheight = 0.054 )
  self . Text_pageVar = StringVar ( value = '100' )
  self . Text_page = Entry ( self . top , text = '100' , textvariable = self . Text_pageVar , font = ( '宋体' , 9 ) )
  self . Text_page . place ( relx = 0.822 , rely = 0.017 , relwidth = 0.047 , relheight = 0.054 )
  self . Check_2Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_2.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_2 = Checkbutton ( self . top , text = 'title' , variable = self . Check_2Var , style = 'Check_2.TCheckbutton' )
  self . Check_2 . place ( relx = 0.708 , rely = 0.104 , relwidth = 0.104 , relheight = 0.043 )
  self . Check_3Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_3.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_3 = Checkbutton ( self . top , text = 'ip' , variable = self . Check_3Var , style = 'Check_3.TCheckbutton' )
  self . Check_3 . place ( relx = 0.833 , rely = 0.104 , relwidth = 0.104 , relheight = 0.043 )
  self . Check_1Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_1.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_1 = Checkbutton ( self . top , text = 'host' , variable = self . Check_1Var , style = 'Check_1.TCheckbutton' )
  self . Check_1 . place ( relx = 0.582 , rely = 0.104 , relwidth = 0.093 , relheight = 0.043 )
  self . Check_5Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_5.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_5 = Checkbutton ( self . top , text = 'port' , variable = self . Check_5Var , style = 'Check_5.TCheckbutton' )
  self . Check_5 . place ( relx = 0.708 , rely = 0.173 , relwidth = 0.093 , relheight = 0.043 )
  self . Check_7Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_7.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_7 = Checkbutton ( self . top , text = 'province' , variable = self . Check_7Var , style = 'Check_7.TCheckbutton' )
  self . Check_7 . place ( relx = 0.582 , rely = 0.242 , relwidth = 0.116 , relheight = 0.043 )
  self . Check_8Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_8.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_8 = Checkbutton ( self . top , text = 'city' , variable = self . Check_8Var , style = 'Check_8.TCheckbutton' )
  self . Check_8 . place ( relx = 0.708 , rely = 0.242 , relwidth = 0.093 , relheight = 0.043 )
  self . Check_4Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_4.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_4 = Checkbutton ( self . top , text = 'domain' , variable = self . Check_4Var , style = 'Check_4.TCheckbutton' )
  self . Check_4 . place ( relx = 0.582 , rely = 0.173 , relwidth = 0.104 , relheight = 0.043 )
  self . Check_10Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_10.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_10 = Checkbutton ( self . top , text = 'header' , variable = self . Check_10Var , style = 'Check_10.TCheckbutton' )
  self . Check_10 . place ( relx = 0.582 , rely = 0.311 , relwidth = 0.116 , relheight = 0.043 )
  self . Check_9Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_9.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_9 = Checkbutton ( self . top , text = 'country_name' , variable = self . Check_9Var , style = 'Check_9.TCheckbutton' )
  self . Check_9 . place ( relx = 0.833 , rely = 0.242 , relwidth = 0.173 , relheight = 0.043 )
  self . Check_11Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_11.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_11 = Checkbutton ( self . top , text = 'server' , variable = self . Check_11Var , style = 'Check_11.TCheckbutton' )
  self . Check_11 . place ( relx = 0.708 , rely = 0.311 , relwidth = 0.116 , relheight = 0.043 )
  self . Check_6Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_6.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_6 = Checkbutton ( self . top , text = 'country' , variable = self . Check_6Var , style = 'Check_6.TCheckbutton' )
  self . Check_6 . place ( relx = 0.833 , rely = 0.173 , relwidth = 0.116 , relheight = 0.043 )
  self . Check_13Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_13.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_13 = Checkbutton ( self . top , text = 'banner' , variable = self . Check_13Var , style = 'Check_13.TCheckbutton' )
  self . Check_13 . place ( relx = 0.582 , rely = 0.38 , relwidth = 0.116 , relheight = 0.043 )
  self . Check_14Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_14.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_14 = Checkbutton ( self . top , text = 'cert' , variable = self . Check_14Var , style = 'Check_14.TCheckbutton' )
  self . Check_14 . place ( relx = 0.708 , rely = 0.38 , relwidth = 0.093 , relheight = 0.043 )
  self . Check_16Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_16.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_16 = Checkbutton ( self . top , text = 'as_number' , variable = self . Check_16Var , style = 'Check_16.TCheckbutton' )
  self . Check_16 . place ( relx = 0.582 , rely = 0.449 , relwidth = 0.127 , relheight = 0.043 )
  self . Check_15Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_15.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_15 = Checkbutton ( self . top , text = 'isp' , variable = self . Check_15Var , style = 'Check_15.TCheckbutton' )
  self . Check_15 . place ( relx = 0.833 , rely = 0.38 , relwidth = 0.161 , relheight = 0.043 )
  self . Check_12Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_12.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_12 = Checkbutton ( self . top , text = 'protocol' , variable = self . Check_12Var , style = 'Check_12.TCheckbutton' )
  self . Check_12 . place ( relx = 0.833 , rely = 0.311 , relwidth = 0.104 , relheight = 0.043 )
  self . Check_17Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_17.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_17 = Checkbutton ( self . top , text = 'as_organization' , variable = self . Check_17Var , style = 'Check_17.TCheckbutton' )
  self . Check_17 . place ( relx = 0.708 , rely = 0.449 , relwidth = 0.207 , relheight = 0.043 )
  self . Check_18Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_18.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_18 = Checkbutton ( self . top , text = 'latitude' , variable = self . Check_18Var , style = 'Check_18.TCheckbutton' )
  self . Check_18 . place ( relx = 0.582 , rely = 0.518 , relwidth = 0.127 , relheight = 0.043 )
  self . Check_19Var = StringVar ( value = '0' )
  self . style . configure ( 'Check_19.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_19 = Checkbutton ( self . top , text = 'longitude' , variable = self . Check_19Var , style = 'Check_19.TCheckbutton' )
  self . Check_19 . place ( relx = 0.708 , rely = 0.518 , relwidth = 0.195 , relheight = 0.043 )
  self . Check_urlVar = StringVar ( value = '0' )
  self . style . configure ( 'Check_url.TCheckbutton' , font = ( '宋体' , 9 ) )
  self . Check_url = Checkbutton ( self . top , text = 'url' , variable = self . Check_urlVar , style = 'Check_url.TCheckbutton' )
  self . Check_url . place ( relx = 0.639 , rely = 0.622 , relwidth = 0.138 , relheight = 0.06 )
  self . style . configure ( 'Command_stop.TButton' , font = ( '宋体' , 9 ) )
  self . Command_stop = Button ( self . top , text = '停止' , command = self . Command_stop_Cmd , style = 'Command_stop.TButton' )
  self . Command_stop . place ( relx = 0.799 , rely = 0.76 , relwidth = 0.127 , relheight = 0.071 )
class II1III ( OooO0OO ) :
 def __init__ ( self , master = None ) :
  OooO0OO . __init__ ( self , master )
  self . Check_1Var . set ( "1" )
  self . Check_2Var . set ( "1" )
  self . Check_3Var . set ( "1" )
  self . Check_4Var . set ( "1" )
  self . Check_5Var . set ( "1" )
  self . Check_10Var . set ( "1" )
  self . Check_11Var . set ( "1" )
  self . Check_12Var . set ( "1" )
  self . Check_13Var . set ( "1" )
  self . Text_pageVar . set ( "1" )
  self . Text_sizeVar . set ( "100" )
 def fofa_search ( self , query_str , fields , size , page = 1 ) :
  Ii11Ii1I = 'https://fofa.info/api/v1/search/all'
  O00oO = {
 'email' : I1Ii ,
 'key' : o0oOo0Ooo0O ,
 'qbase64' : base64 . b64encode ( query_str . encode ( 'utf-8' ) ) . decode ( 'utf-8' ) ,
 'size' : size ,
 'fields' : "," . join ( fields ) ,
 'page' : page
 }
  I11i1I1I = requests . get ( Ii11Ii1I , params = O00oO ) . json ( )
  oO0Oo = I11i1I1I . get ( 'errmsg' )
  if oO0Oo :
   if '401 Unauthorized' in oO0Oo :
    self . Text_out . insert ( INSERT , 'api或邮箱不正确!\n' )
   return
  self . Text_out . insert ( INSERT , "查询参数：{}，当前第{}页，结果数：{}\n" . format ( query_str , page , len ( I11i1I1I . get ( 'results' ) ) ) )
  return I11i1I1I . get ( 'results' )
 def run_search ( self , query_list , fields , size , max_page , check_url ) :
  O0o0 = [ ]
  for OO00Oo in query_list :
   if O0OoOoo00o : break
   for O0OOO0OOoO0O in range ( 1 , max_page + 1 ) :
    if O0OoOoo00o : break
    try :
     O00Oo000ooO0 = self . fofa_search ( OO00Oo , fields , size = size , page = O0OOO0OOoO0O )
    except :
     continue
    if O00Oo000ooO0 :
     for iI111iI in O00Oo000ooO0 :
      if len ( fields ) == 1 :
       OoO0O00IIiII = { fields [ 0 ] : iI111iI }
      else :
       OoO0O00IIiII = dict ( zip ( fields , iI111iI ) )
      OoO0O00IIiII . update ( { 'query_str' : OO00Oo } )
      if check_url :
       OoO0O00IIiII . update ( { 'url' : OoO0O00IIiII [ 'host' ] if 'http' in OoO0O00IIiII [ 'host' ] else "http://" + OoO0O00IIiII [ 'host' ] } )
      O0o0 . append ( OoO0O00IIiII )
    else :
     break
  if O0o0 :
   o0 = time . strftime ( "%Y-%m-%d-%H-%M-%S_fofa_results.xlsx" )
   self . Text_out . insert ( INSERT , "保存到文件：{}\n" . format ( o0 ) )
   Iiii ( o0 , Sheet1 = O0o0 )
   os . startfile ( os . getcwd() )
 def Command_query_Cmd ( self , event = None ) :
  self . Text_out . delete ( '1.0' , 'end' )
  oOOOOo0 = [ OoO0O00IIiII for OoO0O00IIiII in self . Text_query . get ( "0.0" , "end" ) . strip ( ) . split ( '\n' ) if OoO0O00IIiII . strip ( ) != "" ]
  iiII1i1 = self . Text_sizeVar . get ( )
  o00oOO0o = int ( self . Text_pageVar . get ( ) )
  OOO00O = int ( self . Check_urlVar . get ( ) )
  OOoOO0oo0ooO = [ ]
  for O0o0O00Oo0o0 , O00O0oOO00O00 in [ [ self . Check_1 , self . Check_1Var ] , [ self . Check_2 , self . Check_2Var ] , [ self . Check_3 , self . Check_3Var ] , [ self . Check_4 , self . Check_4Var ] , [ self . Check_5 , self . Check_5Var ] , [ self . Check_6 , self . Check_6Var ] , [ self . Check_7 , self . Check_7Var ] , [ self . Check_8 , self . Check_8Var ] , [ self . Check_9 , self . Check_9Var ] , [ self . Check_10 , self . Check_10Var ] , [ self . Check_11 , self . Check_11Var ] , [ self . Check_12 , self . Check_12Var ] , [ self . Check_13 , self . Check_13Var ] , [ self . Check_14 , self . Check_14Var ] , [ self . Check_15 , self . Check_15Var ] , [ self . Check_16 , self . Check_16Var ] , [ self . Check_17 , self . Check_17Var ] , [ self . Check_18 , self . Check_18Var ] , [ self . Check_19 , self . Check_19Var ] ] :
   if int ( O00O0oOO00O00 . get ( ) ) :
    OOoOO0oo0ooO . append ( O0o0O00Oo0o0 [ 'text' ] )
  self . thread_it ( self . run_search , oOOOOo0 , OOoOO0oo0ooO , iiII1i1 , o00oOO0o , OOO00O )
 def Command_stop_Cmd ( self , event = None ) :
  global O0OoOoo00o
  O0OoOoo00o = True
 @ staticmethod
 def thread_it ( func , * args ) :
  oo0ooO0oOOOOo = threading . Thread ( target = func , args = args )
  oo0ooO0oOOOOo . setDaemon ( True )
  oo0ooO0oOOOOo . start ( )
if __name__ == "__main__" :
 OO0oOoOO0oOO0 = Tk ( )
 II1III ( OO0oOoOO0oOO0 ) . mainloop ( )
 try : OO0oOoOO0oOO0 . destroy ( )
 except : pass

