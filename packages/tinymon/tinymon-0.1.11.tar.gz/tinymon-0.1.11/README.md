# Tinymon

## Usage

------------------------------------------------------------------------------

### **TinyMon**

#### class

- TinyMon(baseimagepath=None, fbdev=None, previewdev=None, brightness=15, sleep_time=0.01, timeout=7)
  - parameters
    - baseimagepath
      - background image
      - default None
    - fbdev
      - frame buffer device
      - should use Ssd1362
      - fbdev=Ssd1362()
    - previewdev
      - preview video device
      - experimental
    - brightness
      - 0 ~ 15
    - sleep_time
      - sleep for cpu idle time
      - recommend 0.01
    - timeout
      - timeout for preview udp 
      - default 7 seconds

#### methods

- addctrl(id, ctrl)
  - parameters
    - id : str
      - ctrl name for internal dictionary
    - ctrl : ImageCtrl, TextCtrl
      - ImageCtrl, TextCtrl instance

- delImageCtrl(id)
  - parameters
    - id : str
      - ctrl name for internal dictionary
- delTextCtrl(id)
  - parameters
    - id : str
      - ctrl name for internal dictionary

------------------------------------------------------------------------------

### **ImageCtrl**

#### class

- ImageCtrl(pos=(0,0), size=(MAX_WIDTH,MAX_HEIGHT), path=None)
  - parameters
    - pos : tuple (x,y)
      - image position top-left
    - size : tuple (width, height)
      - image size : max(256, 64)
    - path
      - image path

#### methods

- open(path, pos=None, size=None)
  - description
    - change an image in ctrl instance
  - parameters
    - pos : tuple (x,y)
      - image position top-left
    - size : tuple (width, height)
      - image size : max(256, 64)

- changePos(pos)
  - parameters
    - pos : tuple (x,y)
      - image position top-left

- paste(im, box=(0,0))
  - description
    - pastes another image into this image
  - parameters
    - im
      - pillow image instance
    - box : (x,y), (x, y, width, height)
      - (x, y) : top left position
      - (x, y, width, height) : top left and size

- clear(image)
  - description
    - paste image whole area
    - for background image
  - parameters
    - image
      - pillow image

------------------------------------------------------------------------------

### **TextCtrl**

#### class

- TextCtrl(pos=(10,10) , fontsize=14, font='font/NanumBarunGothicLight.ttf', text=None):
  - parameters
    - pos : tuple (x,y)
      - text position top-left
    - fontsize
    - font
      - font path
    - text : str
      - input text

#### methods

- setText(text)
  - parameters
    - text : str
      - input text

- draw(im=None, fill=255)
  - description
    - for internal use
  - parameters
    - im
      - pillow image
    - fill
      - gray level : 0~255
  - returns
    - pillow image
    - text added image

------------------------------------------------------------------------------

## requirements

### g4l (gpio python package)

>- link : <https://gitlab.com/telelian/peripheral-library/g4l>

### ssd1362-py

>- link : <https://gitlab.com/telelian/peripheral-library/ssd1362.git>
