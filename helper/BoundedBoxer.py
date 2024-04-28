import cv2

class BoundedBoxer:
    def __init__(self, selec,Cert_path) -> None:
        self.ix, self.iy = -1, -1
        self.drawing = False # true if mouse is pressed
        self.rectangles = []
        self.RezeidFacotr = ()
        self.seleccol = selec
        self.Cert_path = Cert_path

    # mouse callback function
    def draw_rectangle(self, event, x, y, flags, param):
        if len(self.rectangles) != len(self.seleccol):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix, self.iy = x, y
            elif event == cv2.EVENT_MOUSEMOVE:
                img_temp = self.img.copy()
                label = self.seleccol[len(self.rectangles) % len(self.seleccol)]
                cv2.putText(img_temp, label, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                
                if self.drawing == True:
                    
                    
                    
                    cv2.rectangle(img_temp, (self.ix, self.iy), (x, y), (0, 255, 0), 2)
                cv2.imshow('image', img_temp)
            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), (0, 255, 0), 2)
                label = self.seleccol[len(self.rectangles) % len(self.seleccol)]
                cv2.putText(self.img, label, (self.ix, self.iy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                x1_orig, y1_orig = self.ix, self.iy
                x2_orig, y2_orig = x, y
                self.rectangles.append(((x1_orig, y1_orig), (x2_orig, y2_orig)))
            

            
    def initiator(self):

        # Load an image
        self.img = cv2.imread(self.Cert_path)  # Replace "Cert_path" with the actual path to the image file
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_rectangle)

        while(1):
            screen_res = 1280, 720  # Replace with your screen resolution
            scale_width = screen_res[0] / self.img.shape[1]
            scale_height = screen_res[1] / self.img.shape[0]
            scale = min(scale_width, scale_height)

            # Resized window width and height
            window_width = int(self.img.shape[1] * scale)
            window_height = int(self.img.shape[0] * scale)
            print(window_width, window_height)
            self.RezeidFacotr = (window_width, window_height)

            # Resize the image
            self.img = cv2.resize(self.img, (window_width, window_height))

            # Display the image
            cv2.imshow('image', self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        # Print the bounding boxes
        for rect in self.rectangles:
            print(rect)
        return self.rectangles, self.RezeidFacotr