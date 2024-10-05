import {ReactNode, lazy} from "react";

// https://ant.design/components/icon-cn/
import { HomeTwoTone, DatabaseTwoTone, VideoCameraTwoTone,
         PlayCircleTwoTone, CameraTwoTone, MoneyCollectTwoTone,
         FileTextTwoTone, ForkOutlined,
         ToolFilled, FilePdfFilled, PictureFilled, PlaySquareFilled } from '@ant-design/icons';

// authorized pages
const HomePage = lazy(()=>import("../pages/HomePage/HomePage"))

const TodoList = lazy(()=>import("../pages/TodoList/TodoList"))

const VideoPlayer = lazy(()=>import("../pages/Media/VideoPlayer/VideoPlayer"))
const ImagePlayer = lazy(()=>import("../pages/Media/ImagePlayer/ImagePlayer"))
const Movies = lazy(()=>import("../pages/Media/Movies/Movies"))

const Trading = lazy(()=>import("../pages/Trading/Trading"))
const ForexTrading = lazy(()=>import("../pages/Trading/Forex/ForexTrading"))
const DigitalCurrency = lazy(()=>import("../pages/Trading/DigitalCurrency/DigitalCurrency"))

const Article = lazy(()=>import("../pages/Article/Article"))
const CloudHandsTrading = lazy(()=>import("../pages/Article/CloundHandsTrading/CloudHandsTrading"))

const Tree = lazy(()=>import("../pages/Tree/Tree"))

const PDFTools = lazy(()=>import("../pages/Tools/PDFTools/PDFTools"))
const PictureTools = lazy(()=>import("../pages/Tools/PictureTools/PictureTools"))
const VideoTools = lazy(()=>import("../pages/Tools/VideoTools/VideoTools"))

// unauthorized pages
const Login = lazy(()=>import("../pages/Login"))
const TestPage = lazy(() =>import("../pages/Test"));
const Page404 = lazy(() =>import("../pages/Page404"));

export interface IRouter {
    id:         string
    title:      string
    path:       string
    exact?:     boolean
    component?: ReactNode
    children?:  IRouter[]
    icon?:      ReactNode
}

export const authrouter: IRouter[] = [
    {   id:         '1',
        path:       '/homepage',
        title:      'HomePage',
        exact:      true,
        component:  <HomePage/>,
        icon:       <HomeTwoTone />
    },
    {   id:         "2",
        path:       '/todolist',
        title:      'Todolist',
        exact:      true,
        component:  <TodoList/>,
        icon:       <DatabaseTwoTone />
    },
    {   id:         "3",
        path:       "/media",
        title:      'Media',
        icon:       <VideoCameraTwoTone />,
        children:   [
            {id:         "3-1",
             path:       '/media/video',
             title:      'VideoPlayer',
             exact:      true,
             component:  <VideoPlayer/>,
             icon:       <PlayCircleTwoTone />
            },
            {id:         "3-2",
             path:       '/media/image',
             title:      'ImagePlayer',
             exact:      true,
             component:  <ImagePlayer/>,
             icon:       <CameraTwoTone />
            },
            {id:         "3-3",
             path:       '/media/movies',
             title:      'Movies',
             exact:      true,
             component:  <Movies/>,
             icon:       <VideoCameraTwoTone />
            },
        ]
    },
    {   id:         "4",
        path:       "/trading",
        title:      'Trading',
        component:  <Trading />,
        icon:       <MoneyCollectTwoTone />,
        children:   [
            {   id:         "41",
                path:       "/trading/forex",
                title:      'Forex',
                component:  <ForexTrading />,
                icon:       <MoneyCollectTwoTone />,
            },
            {   id:         "42",
                path:       "/trading/digitalcurrency",
                title:      'Digital Currency',
                component:  <DigitalCurrency />,
                icon:       <MoneyCollectTwoTone />,
            },
        ]
    },
    {   id:         "5",
        path:       "/article",
        title:      'Article',
        component:  <Article />,
        icon:       <FileTextTwoTone />,
        children: [
            {id:         "51",
             path:       "/article/cloudhandstrading",
             title:      'Clound Hands Weekly Trading Report',
             component:  <CloudHandsTrading />,
             icon:       <FileTextTwoTone />
            },
        ]
    },
    {   id:         "6",
        path:       "/tree",
        title:      'Tree',
        component:  <Tree />,
        icon:       <ForkOutlined />
    },
    {   id:         "7",
        path:       "/tools",
        title:      'Tools',
        icon:      <ToolFilled />,
        children: [
                    {   id:         "7-1",
                        path:       "/tools/pdf",
                        title:      'PDF Tools',
                        component:  <PDFTools />,
                        icon:       <FilePdfFilled />
                    },
                    {   id:         "7-2",
                        path:       "/tools/picture",
                        title:      'Picture Tools',
                        component:  <PictureTools />,
                        icon:       <PictureFilled />
                    },
                    {   id:         "7-3",
                        path:       "/tools/video",
                        title:      'Video Tools',
                        component:  <VideoTools />,
                        icon:       <PlaySquareFilled />
                    },
        ]
    }
]

export const unauthrouter: IRouter[] = [
    {   id:         '0',
        path:       '/login',
        title:      'Login',
        exact:      true,
        component:  <Login/>
    },
    {   id:         '999',
        path:       '/testpage',
        title:      'TestPage',
        exact:      true,
        component:  <TestPage/>
    },
    {   id:         '404',
        path:       '/*',
        title:      'Page404',
        component:  <Page404/>
    }
]

export const router: IRouter[] = [
    ...authrouter,
    ...unauthrouter
]
