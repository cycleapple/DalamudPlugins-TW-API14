using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using System.Text.Json;
var records = new List<object>();
foreach (var line in File.ReadLines(args[0])) {
    if (string.IsNullOrWhiteSpace(line)) continue;
    using var stream = File.OpenRead(line);
    using var pe = new PEReader(stream);
    if (!pe.HasMetadata) continue;
    var md = pe.GetMetadataReader();
    var refs = md.AssemblyReferences.Select(h => md.GetAssemblyReference(h)).ToDictionary(r => md.GetString(r.Name), r => r.Version.ToString());
    var assembly = md.GetAssemblyDefinition();
    records.Add(new { path = line, name = md.GetString(assembly.Name), version = assembly.Version.ToString(), references = refs });
}
Console.WriteLine(JsonSerializer.Serialize(records, new JsonSerializerOptions { WriteIndented = true }));
