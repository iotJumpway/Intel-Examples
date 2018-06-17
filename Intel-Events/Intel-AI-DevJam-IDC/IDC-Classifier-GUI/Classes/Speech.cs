using System;
using Windows.Media.SpeechSynthesis;
using Windows.UI.Xaml.Controls;

namespace IDC_Classifier_GUI.Classes
{
    class Speech
    {
        MediaElement mediaElement = new MediaElement();

        public async void Speak(string text)
        {
            System.Diagnostics.Debug.WriteLine(text);
            SpeechSynthesizer synth = new SpeechSynthesizer();
            
            SpeechSynthesisStream stream = await synth.SynthesizeTextToStreamAsync(text);
            mediaElement.SetSource(stream, stream.ContentType);
            mediaElement.Play();
            mediaElement.Stop();
            synth.Dispose();
        }
    }
}