diff --git a/Player.py b/Player.py
index c4cc3f2..737f2e3 100644
--- a/Player.py
+++ b/Player.py
@@ -40,7 +40,6 @@ class PlayerConnection(LineReceiver):
 
     def connectionLost(self, reason):
         print 'Lost connection to game server.'
-        sys.exit(0)
 
     def handleReceivedData(self, data):
         # Load data into JSON object, let the game handle it
diff --git a/mario_game.py b/mario_game.py
index bf1067e..a11c94c 100644
--- a/mario_game.py
+++ b/mario_game.py
@@ -1,5 +1,6 @@
 import sys
 import pygame
+from twisted.internet import reactor
 
 # Class to handle the pygame, gets data from server and updates accordingly
 class MarioKart():
@@ -88,7 +89,7 @@ class MarioKart():
 	def game_tick(self):
 		for event in pygame.event.get():
 			if event.type == pygame.QUIT:
-				self.sendData(-1)
+				reactor.stop()
 			if event.type == pygame.KEYDOWN:
 				if event.key >= 273 and event.key <= 276:
 					# this is a movement key
