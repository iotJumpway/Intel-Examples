using IDC_Classifier_GUI.Classes;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using System.Threading.Tasks;
using Windows.Graphics.Imaging;
using Windows.Storage;
using Windows.Storage.Pickers;
using Windows.Storage.Search;
using Windows.Storage.Streams;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Media.Imaging;

namespace IDC_Classifier_GUI
{
    /// <summary>
    /// Classification gallery
    /// </summary>
    public sealed partial class AppHome : Page
    {
        private GlobalData GlobalData = new GlobalData();
        private Speech Speech = new Speech();

        public AppHome()
        {
            this.InitializeComponent();
            Speech.Speak("Images loading");
            this.DisplayAllFiles();
        }

        private async Task ClassifyAllFiles()
        {
            Debug.WriteLine("-- GETTING FILES");
            StorageFolder appInstalledFolder = Windows.ApplicationModel.Package.Current.InstalledLocation;

            StorageFolder dataFolder = await appInstalledFolder.GetFolderAsync(GlobalData.dataFolder);
            IReadOnlyList<StorageFile> fileList = await dataFolder.GetFilesAsync();

            var result = new ObservableCollection<BitmapImage>();
            Speech.Speak("Processing of images for Invasive Ductal Carcinoma initiating");
            Debug.WriteLine(" ");
            int received = 0; 
            int counter = 0;
            int identified = 0;
            int incorrect = 0;
            int unsure = 0;
            int tns = 0;
            int fps = 0;
            int fns = 0;
            foreach (StorageFile file in fileList)
            {
                Debug.WriteLine(file.Name);
                IBuffer buffer = await FileIO.ReadBufferAsync(file);
                byte[] bytes = buffer.ToArray();
                Stream streamer = new MemoryStream(bytes);
                Windows.Web.Http.HttpStreamContent streamContent = new Windows.Web.Http.HttpStreamContent(streamer.AsInputStream());

                var myFilter = new Windows.Web.Http.Filters.HttpBaseProtocolFilter();
                myFilter.AllowUI = false;
                var client = new Windows.Web.Http.HttpClient(myFilter);
                Windows.Web.Http.HttpResponseMessage results = await client.PostAsync(new Uri(GlobalData.protocol + GlobalData.ip + ":" + GlobalData.port + GlobalData.endpointIDC), streamContent);
                string stringReadResult = await results.Content.ReadAsStringAsync();
                Debug.WriteLine(stringReadResult);

                JToken token = JObject.Parse(stringReadResult);
                received = (int)token.SelectToken("Results");
                double confidence = (double)token.SelectToken("Confidence");
                string Response = (string)token.SelectToken("ResponseMessage");

                if (received != 0)
                {
                    if (file.Name.Contains("class1"))
                    {
                        if (confidence >= GlobalData.threshold)
                        {
                            Debug.WriteLine("CORRECT: IDC correctly detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                            Debug.WriteLine(" ");
                            identified = identified + 1;
                        }
                        else
                        {
                            Debug.WriteLine("UNSURE: IDC detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                            unsure = unsure + 1;
                        }
                    }
                    else
                    {
                        if (confidence >= GlobalData.threshold)
                        { 
                            Debug.WriteLine("FALSE POSITIVE: IDC incorrectly detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                            fps = fps + 1;
                            incorrect = incorrect + 1;
                        }
                        else
                        {
                            Debug.WriteLine("UNSURE: IDC detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                            unsure = unsure + 1;
                        }
                    }
                    Speech.Speak("Processed image " + (counter + 1));

                }
                else
                {
                    if (file.Name.Contains("class0"))
                    {
                        Debug.WriteLine("CORRECT: IDC correctly not detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                        tns = tns + 1;

                    }
                    else
                    {
                        if (confidence >= GlobalData.threshold)
                        {
                            Debug.WriteLine("FALSE NEGATIVE: IDC incorrectly not detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                            fns = fns + 1;
                            incorrect = incorrect + 1;
                        }
                        else
                        {
                            Debug.WriteLine("UNSURE: IDC not detected in image " + (counter + 1) + " " + file.Name + " with " + confidence + " confidence.");
                            unsure = unsure + 1;
                        }
                        
                    }
                    Speech.Speak("Processed image " + (counter + 1));
                    Debug.WriteLine(" ");
                }
                counter++;
                if (counter == (GlobalData.expectedCount*2))
                {
                    double actualIdentified = (double)identified;
                    double accuracy = (((double)tns + actualIdentified) / (actualIdentified + (double)fps)) / ((double)counter - unsure);
                    double precision = actualIdentified / (actualIdentified + (double)fps);
                    double recall = actualIdentified / (actualIdentified + (double)fns);
                    double fscore = 2 * ((double)precision * (double)recall / ((double)precision + (double)recall));

                    Speech.Speak(identified + " true positives, " + fps + " false positives, " + fns + " false negatives, " + unsure + " unsure, " + tns + " true negatives, " + incorrect + " incorrect examples classified, " + Math.Round(accuracy, 2) + " accuracy, " + Math.Round(precision, 2) + " precision, " + Math.Round(recall, 2) + " recall, " + Math.Round(fscore, 2) + " fscore");

                    Debug.WriteLine(" ");
                    Debug.WriteLine("- " + identified  + " true positives, " + fps + " false positives, " + fns + " false negatives, " + tns + " true negatives");
                    Debug.WriteLine("- " + unsure + " unsure");
                    Debug.WriteLine("- " + incorrect + " incorrect examples classified");
                    Debug.WriteLine("- " + Math.Round(accuracy, 2) + " accuracy");
                    Debug.WriteLine("- " + Math.Round(precision, 2) + " precision");
                    Debug.WriteLine("- " + Math.Round(recall, 2) + " recall");
                    Debug.WriteLine("- " + Math.Round(fscore, 2) + " fscore");
                }
                System.Threading.Thread.Sleep(1000);
            }
        }
        private async Task DisplayAllFiles()
        {
            Debug.WriteLine("-- GETTING FILES");
            StorageFolder appInstalledFolder = Windows.ApplicationModel.Package.Current.InstalledLocation;
            StorageFolder dataFolder = await appInstalledFolder.GetFolderAsync(GlobalData.dataFolder);
            IReadOnlyList<StorageFile> fileList = await dataFolder.GetFilesAsync();

            this.ImageHolder.Opacity = 0;
            this.ImageHolder.Width = 1500;
            this.ImageHolder.Height = 1500;

            this.ImageHolder.ColumnDefinitions.Add(new ColumnDefinition() { Width = GridLength.Auto });
            this.ImageHolder.ColumnDefinitions.Add(new ColumnDefinition() { Width = new GridLength() });
            this.ImageHolder.ColumnDefinitions.Add(new ColumnDefinition() { Width = new GridLength() });
            this.ImageHolder.ColumnDefinitions.Add(new ColumnDefinition() { Width = new GridLength() });
            this.ImageHolder.ColumnDefinitions.Add(new ColumnDefinition() { Width = new GridLength() });
            this.ImageHolder.ColumnDefinitions.Add(new ColumnDefinition() { Width = new GridLength() });
            this.ImageHolder.RowDefinitions.Add(new RowDefinition() { Height = new GridLength() });

            Button button = new Button();
            button.Name = "IDC_Classify";
            button.Content = "Classify All Images";
            button.Click += IDC_Classify_Click;
            button.Width = 250;
            button.Height = 75;
            button.Foreground = new SolidColorBrush(Windows.UI.Colors.White);
            button.SetValue(Grid.ColumnProperty, 6);
            button.SetValue(Grid.RowProperty, 0);
            this.ImageHolder.Children.Add(button);

            this.ImageHolder.RowDefinitions.Add(new RowDefinition() { Height = new GridLength() });

            var result = new ObservableCollection<BitmapImage>();
            var i = 0;
            var row = 1;
            var column = 0;
            foreach (StorageFile file in fileList)
            {
                Debug.WriteLine(file.Name);
                using (var stream = await file.OpenAsync(FileAccessMode.Read))
                {
                    var bitmapDecoder = await BitmapDecoder.CreateAsync(stream);
                    var pixelProvider = await bitmapDecoder.GetPixelDataAsync();
                    var bits = pixelProvider.DetachPixelData();
                    var softwareBitmap = new SoftwareBitmap(
                      BitmapPixelFormat.Bgra8,
                      (int)bitmapDecoder.PixelWidth,
                      (int)bitmapDecoder.PixelHeight,
                      BitmapAlphaMode.Premultiplied);
                    softwareBitmap.CopyFromBuffer(bits.AsBuffer());

                    var softwareBitmapSource = new SoftwareBitmapSource();
                    await softwareBitmapSource.SetBitmapAsync(softwareBitmap);

                    var source = new SoftwareBitmapSource();
                    await source.SetBitmapAsync(softwareBitmap);

                    if (i != 0 && i % 6 == 0)
                    {
                        Debug.WriteLine("-- New Image Row "+ row);
                        this.ImageHolder.RowDefinitions.Add(
                            new RowDefinition() { Height = GridLength.Auto });
                        column = 0;
                        row++;
                    }

                    Image image = new Image();
                    image.Source = softwareBitmapSource;
                    image.Name = file.Name;
                    image.Width = 250;
                    image.Height = 250;
                    image.SetValue(Grid.ColumnProperty, column);
                    image.SetValue(Grid.RowProperty, row);
                    this.ImageHolder.Children.Add(image);

                    column++;
                    i++;
                }
            }
            this.ImageHolder.Opacity = 1;

        }
        private async Task GetFolders()
        {
            Debug.WriteLine("-- GETTING FOLDERS");
            StorageFolder appInstalledFolder = Windows.ApplicationModel.Package.Current.InstalledLocation;
            StorageFolder dataFolder = await appInstalledFolder.GetFolderAsync("Data");
            IReadOnlyList<StorageFolder> folderList = await dataFolder.GetFoldersAsync();

            foreach (StorageFolder folder in folderList)
            {
                Debug.WriteLine(folder.DisplayName);
            }

        }
        private async Task ChooseImages()
        {

            Debug.WriteLine("-- CHOOSE IMAGES");
            FolderPicker folderpicker = new FolderPicker();
            folderpicker.FileTypeFilter.Add("*");
            StorageFolder tmpfolder = await folderpicker.PickSingleFolderAsync();
            QueryOptions options;

            options = new QueryOptions(CommonFileQuery.DefaultQuery, new[] { ".png", ".jpg", ".bmp", ".tiff", ".jpeg", ".gif" });
            options.FolderDepth = FolderDepth.Deep;
            StorageFileQueryResult k = tmpfolder.CreateFileQueryWithOptions(options);
            IReadOnlyList<StorageFile> image_files = await k.GetFilesAsync();

        }
        public async static Task<byte[]> ImageToBytes(BitmapImage image)
        {
            RandomAccessStreamReference streamRef = RandomAccessStreamReference.CreateFromUri(image.UriSource);
            IRandomAccessStreamWithContentType streamWithContent = await streamRef.OpenReadAsync();
            byte[] buffer = new byte[streamWithContent.Size];
            await streamWithContent.ReadAsync(buffer.AsBuffer(), (uint)streamWithContent.Size, InputStreamOptions.None);
            return buffer;
        }

        private void Camera_Click(object sender, RoutedEventArgs e)
        {
            this.Frame.Navigate(typeof(MainPage));
        }

        private void Home_Click(object sender, RoutedEventArgs e)
        {
            this.Frame.Navigate(typeof(AppHome));
        }

        private void IDC_Classify_Click(object sender, RoutedEventArgs e)
        {
            ClassifyAllFiles();
        }
        

        private void HamburgerButton_Click(object sender, RoutedEventArgs e)
        {
            MySplitView.IsPaneOpen = !MySplitView.IsPaneOpen;
        }
    }
}
