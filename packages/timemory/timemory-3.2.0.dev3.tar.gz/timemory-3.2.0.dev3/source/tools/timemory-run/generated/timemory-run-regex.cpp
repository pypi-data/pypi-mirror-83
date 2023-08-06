// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//

#include <regex>
#include <string>

extern "C" bool
timemory_source_file_constraint(const std::string& fname)
{
    static auto regex_opts =
        std::regex_constants::ECMAScript | std::regex_constants::optimize;
    // clang-format off
    //
    std::regex file_regex("^(elf_ops.c|gotcha.c|gotcha_auxv.c|gotcha_dl.c|gotcha_utils.c|hash.c|libc_wrappers.c|library_filters.c|tool.c|translations.c|Annotation.cpp|AnnotationBinding.cpp|Blackboard.cpp|Caliper.cpp|ChannelController.cpp|ConfigManager.cpp|MemoryPool.cpp|MetadataTree.cpp|RegionProfile.cpp|SnapshotRecord.cpp|api.cpp|builtin_configmanager.cpp|cali.cpp|cali_datatracker.cpp|config_sanity_check.cpp|CudaActivityController.cpp|HatchetRegionProfileController.cpp|HatchetSampleProfileController.cpp|RuntimeReportController.cpp|controllers.cpp|machine_mpi.cpp|machine_serial.cpp|setup_mpi.cpp|setup_serial.cpp|Attribute.cpp|CaliperMetadataAccessInterface.cpp|CompressedSnapshotRecord.cpp|Entry.cpp|Log.cpp|Node.cpp|NodeBuffer.cpp|OutputStream.cpp|RuntimeConfig.cpp|SnapshotBuffer.cpp|SnapshotTextFormatter.cpp|StringConverter.cpp|Variant.cpp|cali_types.c|cali_variant.c|format_util.cpp|parse_util.cpp|unitfmt.c|vlenc.c|BufferedRegionProfile.cpp|utilCaliper.cpp|wrapAnnotation.cpp|wrapBufferedRegionProfile.cpp|wrapCaliper.cpp|wrapConfigManager.cpp|wrapScopeAnnotation.cpp|aggregate_over_mpi.cpp|LoopReportController.cpp|SpotController.cpp|SpotV1Controller.cpp|mpi_machine.cpp|mpi_setup.cpp|MpiReport.cpp|MpitServiceMPI.cpp|MpiTracing.cpp|MpiWrap.cpp|tau.cpp|Aggregator.cpp|CalQLParser.cpp|CaliReader.cpp|CaliWriter.cpp|CaliperMetadataDB.cpp|Expand.cpp|FlatExclusiveRegionProfile.cpp|FlatInclusiveRegionProfile.cpp|FormatProcessor.cpp|JsonFormatter.cpp|JsonSplitFormatter.cpp|NestedExclusiveRegionProfile.cpp|NestedInclusiveRegionProfile.cpp|Preprocessor.cpp|QueryProcessor.cpp|QuerySpec.cpp|RecordSelector.cpp|SnapshotTree.cpp|TableFormatter.cpp|TreeFormatter.cpp|UserFormatter.cpp|Services.cpp|AdiakExport.cpp|AdiakImport.cpp|Aggregate.cpp|AggregationDB.cpp|AllocService.cpp|Callpath.cpp|CpuInfo.cpp|Cupti.cpp|CuptiEventSampling.cpp|CuptiTrace.cpp|Debug.cpp|EnvironmentInfo.cpp|EventTrigger.cpp|InstLookup.cpp|callbacks.c|curious.c|dynamic_array.c|file_registry.c|mount_tree.c|wrappers.c|IOService.cpp|KokkosLookup.cpp|KokkosProfilingSymbols.cpp|KokkosTime.cpp|Libpfm.cpp|perf_postprocessing.cpp|perf_util.c|MemUsageService.cpp|LoopMonitor.cpp|RegionMonitor.cpp|ThreadMonitor.cpp|NVProf.cpp|OmptService.cpp|Papi.cpp|Pcp.cpp|PcpMemory.cpp|PthreadService.cpp|Recorder.cpp|Report.cpp|Sampler.cpp|Sos.cpp|Spot.cpp|Statistics.cpp|LookupDlAddr.cpp|LookupDyninst.cpp|SymbolLookup.cpp|SysAllocService.cpp|TextLog.cpp|Timestamp.cpp|IntelTopdown.cpp|Trace.cpp|TraceBufferChunk.cpp|validator.cpp|VTuneBindings.cpp|AttributeExtract.cpp|cali-query.cpp|query_common.cpp|cali-stat.cpp|mpi-caliquery.cpp|Args.cpp|performance.cpp|sandbox.cpp|sandbox_json.cpp|sandbox_rtti.cpp|base.cpp|derived.cpp|sandbox_vs.cpp|timers.c|unset_trace.c|kokkosp.cpp|library.cpp|libpytimemory-api.cpp|libpytimemory-auto-timer.cpp|libpytimemory-component-bundle.cpp|libpytimemory-component-list.cpp|libpytimemory-components.cpp|libpytimemory-enumeration.cpp|libpytimemory-hardware-counters.cpp|libpytimemory-profile.cpp|libpytimemory-rss-usage.cpp|libpytimemory-settings.cpp|libpytimemory-signals.cpp|libpytimemory-trace.cpp|libpytimemory-units.cpp|libpytimemory.cpp|extern.cpp|read_bytes.cpp|read_char.cpp|written_bytes.cpp|written_char.cpp|current_peak_rss.cpp|kernel_mode_time.cpp|num_io_in.cpp|num_io_out.cpp|num_major_page_faults.cpp|num_minor_page_faults.cpp|page_rss.cpp|peak_rss.cpp|priority_context_switch.cpp|user_mode_time.cpp|virtual_memory.cpp|voluntary_context_switch.cpp|complete_list.cpp|full_auto_timer.cpp|minimal_auto_timer.cpp|extern.cu|settings.cpp|vsettings.cpp|popen.cpp|component_bundle.cpp|component_hybrid.cpp|component_list.cpp|component_tuple.cpp|lightweight_tuple.cpp|timemory_c.c|timemory_c.cpp|kp_timemory.cpp|kp_timemory_common.cpp|kp_timemory_filter.cpp|sample.cpp|timem.cpp|timemory-avail.cpp|timemory-mpip.cpp|timemory-ncclp.cpp|timemory-ompt.cpp|timemory-pid.cpp|timemory-run-regex.cpp|timemory-run-details.cpp|timemory-run-fork.cpp|timemory-run.cpp|trace.cpp)$", regex_opts);
    return std::regex_search(fname, file_regex);
    //
    // clang-format on
}
